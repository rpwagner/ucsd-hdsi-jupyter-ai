"""Real Jupyter MCP + JSD + Goose ACP against a synthetic model, never a provider.

Run inside the image in CI. WEEK3_SKIP_KERNEL=1 is local-host diagnostics only.
"""
import asyncio
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time

import httpx
import websockets
from jupyterlab_chat.models import Message
from jupyterlab_chat.ychat import YChat
from traitlets.config import LoggingConfigurable

from week3_chat import ModelChatPersona
from week3_chat.mcp_persona import NotebookMcpPersona, mcp_client, TOOLS
from week3_chat.goose_persona import GooseWorkshopPersona

ROOT = Path(__file__).resolve().parents[1]


class Fixture(BaseHTTPRequestHandler):
    calls = []
    scenario = 'read'
    catalogs = []

    def log_message(self, *args):
        pass

    def do_GET(self):
        Fixture.calls.append(('GET', self.path))
        self.send_error(400)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        Fixture.calls.append(('POST', self.path))
        assert self.path == '/v1/chat/completions', self.path
        assert body['model'] == 'gpt-oss:20b'
        tools = {t['function']['name']: t for t in body.get('tools', [])}
        Fixture.catalogs.append(list(tools))
        # Evaluate only tool results since the last user turn, not prior turns.
        messages = body['messages']
        last_user = max((i for i, m in enumerate(messages) if m['role'] == 'user'), default=-1)
        results = [m for m in messages[last_user + 1:] if m['role'] == 'tool']
        desired = None
        args = {}
        if tools:
            if not results:
                desired = 'read_demo_cell'
            elif len(results) == 1 and Fixture.scenario in ('edit', 'run'):
                desired = 'set_demo_value' if Fixture.scenario == 'edit' else 'run_demo_cell'
                # The controlled test changes 6 → 8 and then executes 8.
                args = {'value': 8, 'expected_value': 6} if desired == 'set_demo_value' else {'expected_value': 8}
        name = next((n for n in tools if desired and n.endswith(desired)), None)
        call = None
        if name:
            call = {'id': f'fixture-{len(Fixture.calls)}', 'type': 'function',
                    'function': {'name': name, 'arguments': json.dumps(args)}}
        message = {'role': 'assistant', 'content': None if call else 'SYNTHETIC FIXTURE: reviewed arithmetic task complete.'}
        if call:
            message['tool_calls'] = [call]
        if body.get('stream'):
            delta = dict(message)
            if call:
                delta['tool_calls'][0]['index'] = 0
            chunks = [
                {'id': 'synthetic', 'object': 'chat.completion.chunk', 'created': 0,
                 'model': body['model'], 'choices': [{'index': 0, 'delta': delta, 'finish_reason': None}]},
                {'id': 'synthetic', 'object': 'chat.completion.chunk', 'created': 0,
                 'model': body['model'], 'choices': [{'index': 0, 'delta': {},
                                                    'finish_reason': 'tool_calls' if call else 'stop'}]}]
            data = ''.join('data: ' + json.dumps(c) + '\n\n' for c in chunks) + 'data: [DONE]\n\n'
            content_type = 'text/event-stream'
        else:
            data = json.dumps({'id': 'synthetic', 'object': 'chat.completion', 'created': 0,
                               'model': body['model'], 'choices': [{'index': 0, 'message': message,
                                                                  'finish_reason': 'tool_calls' if call else 'stop'}]})
            content_type = 'application/json'
        encoded = data.encode()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


class Manager(LoggingConfigurable):
    def __init__(self, root, chat):
        super().__init__()
        self.root_dir = str(root)
        self.chat = chat
        self.event_loop = asyncio.get_running_loop()
        self.event_logger = None

    def get_chat_dir(self):
        return self.root_dir

    def get_workspace_dir(self):
        return self.root_dir

    def get_dotjupyter_dir(self):
        return None


def new_persona(cls, root):
    chat = YChat()
    chat.initial_path = 'fixture.chat'
    return cls(chat=chat, parent=Manager(root, chat))


def message(body):
    return Message(id=str(time.monotonic()), body=body, time=0, sender='human')


async def permission_driver(persona, decisions, deny=False):
    client = await persona.get_client()
    while True:
        for (session_id, tool_id), pending in list(client._permission_manager._pending.items()):
            if pending.future.done():
                continue
            kinds = {o.kind: o.option_id for o in pending.options}
            choice = 'reject_once' if deny else 'allow_once'
            assert choice in kinds, kinds
            assert client.resolve_permission(session_id, tool_id, kinds[choice])
            decisions.append(choice)
        await asyncio.sleep(0.01)


async def checks(work, client):
    async with mcp_client() as mcp:
        assert {t.name for t in await mcp.list_tools()} == TOOLS
        read = (await mcp.call_tool('read_demo_cell', {})).data
        assert read['value'] == 6, read
        # Invalid/stale arguments must fail without changing the live document.
        for args in ({'value': 9, 'expected_value': 6}, {'value': 8, 'expected_value': 8}):
            try:
                await mcp.call_tool('set_demo_value', args)
            except Exception:
                pass
            else:
                raise AssertionError('Invalid edit was admitted')
        assert (await mcp.call_tool('read_demo_cell', {})).data['value'] == 6
    print('PASS: actual MCP catalog and JSD read; invalid/stale edits refused', flush=True)
    if os.environ.get('WEEK3_SKIP_KERNEL') != '1':
        async with mcp_client() as mcp:
            assert (await mcp.call_tool('run_demo_cell', {'expected_value': 6})).data['output'] == '12'

    model_only = new_persona(ModelChatPersona, work)
    await model_only.process_message(message('Explain the arithmetic.'))
    assert any('SYNTHETIC FIXTURE' in m.body for m in model_only.chat.get_messages())
    assert not Fixture.catalogs[-1], 'Model-only persona was given tools'

    p = new_persona(NotebookMcpPersona, work)
    Fixture.scenario = 'edit'
    await p.process_message(message('Read the cell and change 6 to 8.'))
    assert p.pending, str(p.chat.get_messages())
    await p.process_message(message('deny'))
    async with mcp_client() as mcp:
        assert (await mcp.call_tool('read_demo_cell', {})).data['value'] == 6
    await p.process_message(message('Read the cell and change 6 to 8.'))
    assert p.pending
    await p.process_message(message('approve'))
    async with mcp_client() as mcp:
        assert (await mcp.call_tool('read_demo_cell', {})).data['value'] == 8
    if os.environ.get('WEEK3_SKIP_KERNEL') != '1':
        for _ in range(50):
            saved = (await client.get('/api/contents/demo.ipynb')).json()['content']
            if '[2, 4, 8]' in ''.join(saved['cells'][1]['source']):
                break
            await asyncio.sleep(0.1)
        observed = await asyncio.create_subprocess_exec(sys.executable, str(ROOT / 'container/inspect_lesson.py'),
                                                       stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        output, error = await observed.communicate()
        assert observed.returncode == 0, error.decode()
        for expected in (b'last value = 8', b'Saved output: 12', b'Live kernel total: 12'):
            assert expected in output, output
        print('PASS: independent post-edit state is source 8 / saved output 12 / live kernel 12', flush=True)
    # Approval cannot be replayed.
    await p.process_message(message('approve'))
    assert 'No action' in p.chat.get_messages()[-1].body
    print('PASS: model-only preserved; MCP persona deny/approve/replay through real MCP and JSD', flush=True)

    if os.environ.get('WEEK3_SKIP_KERNEL') != '1':
        Fixture.scenario = 'run'
        await p.process_message(message('Read and run the cell.'))
        assert p.pending
        await p.process_message(message('approve'))
        async with mcp_client() as mcp:
            assert (await mcp.call_tool('read_demo_cell', {})).data['output'].strip() == '14'
        print('PASS: real JSD kernel execution and notebook output 14', flush=True)

    # Restore source for the external-agent comparison through the same MCP tool.
    async with mcp_client() as mcp:
        await mcp.call_tool('set_demo_value', {'value': 6, 'expected_value': 8})
        if os.environ.get('WEEK3_SKIP_KERNEL') != '1':
            await mcp.call_tool('run_demo_cell', {'expected_value': 6})
    Fixture.scenario = 'edit'
    goose = new_persona(GooseWorkshopPersona, work)
    before = len(Fixture.calls)
    await asyncio.wait_for(goose.prepare(), timeout=45)
    assert len(Fixture.calls) == before, 'Goose startup contacted the model service'
    denied = []
    driver = asyncio.create_task(permission_driver(goose, denied, deny=True))
    try:
        await asyncio.wait_for(goose.process_message(message('Read and change 6 to 8.')), timeout=90)
    finally:
        driver.cancel()
    assert denied, 'The ACP denial path did not request a permission decision'
    async with mcp_client() as mcp:
        assert (await mcp.call_tool('read_demo_cell', {})).data['value'] == 6
    print('PASS: real Goose ACP startup (no provider query) and permission denial', flush=True)
    allowed = []
    driver = asyncio.create_task(permission_driver(goose, allowed))
    try:
        await asyncio.wait_for(goose.process_message(message('Read and change 6 to 8.')), timeout=90)
    finally:
        driver.cancel()
    assert allowed, 'The ACP edit did not require permission'
    async with mcp_client() as mcp:
        result = (await mcp.call_tool('read_demo_cell', {})).data
        assert result['value'] == 8, (result, str(goose.chat.get_messages()))
    print('PASS: real Goose ACP → model fixture → MCP → JSD edit', flush=True)
    if os.environ.get('WEEK3_SKIP_KERNEL') != '1':
        Fixture.scenario = 'run'
        driver = asyncio.create_task(permission_driver(goose, []))
        try:
            await asyncio.wait_for(goose.process_message(message('Read and run the cell.')), timeout=90)
        finally:
            driver.cancel()
        async with mcp_client() as mcp:
            assert (await mcp.call_tool('read_demo_cell', {})).data['output'].strip() == '14'
        print('PASS: Goose ACP/MCP real kernel execution and output 14', flush=True)
    print('Goose model-visible tools:', json.dumps(Fixture.catalogs[-1]), flush=True)
    assert {n.split('__')[-1] for n in Fixture.catalogs[-1]} == TOOLS, Fixture.catalogs[-1]
    assert not any(method == 'GET' for method, _ in Fixture.calls), Fixture.calls
    await goose.shutdown()
    # Observe the saved file independently, then reset through the normal CLI.
    for _ in range(50):
        saved = (await client.get('/api/contents/demo.ipynb')).json()['content']
        if '8' in ''.join(saved['cells'][1]['source']):
            break
        await asyncio.sleep(0.1)
    else:
        raise AssertionError('JSD did not save the edited document')
    inspected = await asyncio.create_subprocess_exec(sys.executable, str(ROOT / 'container/inspect_lesson.py'),
                                                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    output, error = await inspected.communicate()
    assert inspected.returncode == 0, error.decode()
    assert b'last value = 8' in output, output
    if os.environ.get('WEEK3_SKIP_KERNEL') != '1':
        assert b'Live kernel total: 14' in output, output
    reset = await asyncio.create_subprocess_exec(sys.executable, str(ROOT / 'container/lesson_reset.py'),
                                                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    output, error = await reset.communicate()
    assert reset.returncode == 0, error.decode()
    for _ in range(50):
        async with mcp_client() as mcp:
            reset_state = (await mcp.call_tool('read_demo_cell', {})).data
        if reset_state['value'] == 6 and reset_state['output'] is None:
            break
        await asyncio.sleep(0.1)
    else:
        raise AssertionError('Reset did not reach the live JSD document')
    print('PASS: independent saved-file/kernel inspection and in-place lesson reset', flush=True)


async def run(work, proc):
    async with httpx.AsyncClient(base_url='http://127.0.0.1:8888', trust_env=False,
                                 headers={'Authorization': 'token fixture-only-token'}, timeout=45) as client:
        for _ in range(150):
            try:
                status = await client.get('/api/status')
                if status.status_code == 200:
                    break
            except httpx.ConnectError:
                pass
            if proc.poll() is not None:
                raise RuntimeError('Jupyter exited during startup')
            await asyncio.sleep(0.1)
        else:
            raise TimeoutError('Jupyter not ready')
        response = await client.post('/api/fileid/index', params={'path': 'demo.ipynb'})
        response.raise_for_status()
        file_id = response.json()['id']
        url = f'ws://127.0.0.1:8888/api/collaboration/room/json:notebook:{file_id}?token=fixture-only-token'
        async with websockets.connect(url) as ws:
            from pycrdt import Doc, create_sync_message
            await ws.send(create_sync_message(Doc()))
            await asyncio.wait_for(ws.recv(), timeout=15)
            if os.environ.get('WEEK3_SKIP_KERNEL') != '1':
                response = await client.post('/api/sessions', json={'path': 'demo.ipynb', 'type': 'notebook',
                                                                    'name': 'demo.ipynb', 'kernel': {'name': 'python3'}})
                response.raise_for_status()
            if os.environ.get('WEEK3_UI_SCRIPT'):
                Fixture.scenario = 'edit'
                browser = await asyncio.create_subprocess_exec(
                    os.environ.get('NODE_EXECUTABLE', 'node'), os.environ['WEEK3_UI_SCRIPT'])
                assert await browser.wait() == 0, 'Browser UI check failed'
            await checks(work, client)


def main():
    # Bind first, before any client can mistake a real Ollama for this fixture.
    fixture = ThreadingHTTPServer(('127.0.0.1', 11434), Fixture)
    thread = threading.Thread(target=fixture.serve_forever, daemon=True)
    thread.start()
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        work = root / 'work'
        work.mkdir()
        shutil.copy2(ROOT / 'demo.ipynb', work / 'demo.ipynb')
        os.environ.update(DEMO_PROVIDER_APPROVED='yes', DEMO_API_BASE='http://127.0.0.1:11434/v1/',
                          GOOSE_PATH_ROOT=str(root / 'goose'), FASTMCP_CHECK_FOR_UPDATES='off',
                          FASTMCP_SHOW_SERVER_BANNER='false')
        spec = importlib.util.spec_from_file_location('launch', ROOT / 'container/launch.py')
        launch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(launch)
        launch.prepare_goose()
        env = {**os.environ, 'JUPYTER_CONFIG_DIR': str(root / 'config'), 'JUPYTER_DATA_DIR': str(root / 'data'),
               'JUPYTER_RUNTIME_DIR': str(root / 'runtime')}
        os.environ.update(env)
        command = [sys.executable, '-m', 'jupyterlab', '--config=' + str(ROOT / 'container/jupyter_server_config.py'),
                   '--ServerApp.root_dir=' + str(work), '--ServerApp.ip=127.0.0.1',
                   '--ServerApp.allow_root=True', '--IdentityProvider.token=fixture-only-token']
        with (root / 'server.log').open('w') as log:
            proc = subprocess.Popen(command, cwd=work, env=env, stdout=log, stderr=log)
            try:
                asyncio.run(run(work, proc))
            except BaseException:
                print((root / 'server.log').read_text()[-8000:], file=sys.stderr)
                raise
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                fixture.shutdown()
                fixture.server_close()
    print('PASS: synthetic end-to-end progression; no actual model provider queried.', flush=True)


if __name__ == '__main__':
    main()

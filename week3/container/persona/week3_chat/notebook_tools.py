"""Three deliberately small teaching tools, served by jupyter-server-mcp.

JSD owns the document and kernel. There is no arbitrary path/code parameter.
"""

import asyncio
from pathlib import Path
from typing import Literal

from jupyter_ai_tools.utils import get_file_id, get_jupyter_ydoc, get_room, get_serverapp
from jupyter_ai_tools.toolkits.notebook import edit_cell
from jupyter_server_documents.rooms.ynotebook_room import _source_hash

NOTEBOOK = "demo.ipynb"
CELL = "small-task"
LOCK = asyncio.Lock()


def source(value):
    return f"values = [2, 4, {value}]\ntotal = sum(values)\nprint(total)\n"


async def document():
    root = Path(get_serverapp().root_dir).resolve()
    path = root / NOTEBOOK
    if path.is_symlink() or path.resolve().parent != root:
        raise ValueError("The demonstration notebook must be a regular workspace file.")
    file_id = await get_file_id(str(path))
    if not file_id:
        raise ValueError("Open demo.ipynb and select its Python kernel first.")
    room = await get_room(f"json:notebook:{file_id}")
    ydoc = await get_jupyter_ydoc(file_id)
    if room is None or ydoc is None:
        raise ValueError("Open demo.ipynb first.")
    cells = [c for c in ydoc.ycells if c.get("id") == CELL]
    if len(cells) != 1 or cells[0].get("cell_type") != "code":
        raise ValueError("Reset the demonstration: its arithmetic cell is missing.")
    cell = cells[0]
    text = str(cell.get("source", ""))
    value = next((v for v in (6, 8) if text == source(v)), None)
    if value is None:
        raise ValueError("Only the reviewed arithmetic cell can be used. Reset the demonstration.")
    return room, ydoc, cell, value


async def read_demo_cell() -> dict:
    """Read the reviewed arithmetic cell in demo.ipynb; no other file is accessible."""
    async with LOCK:
        _, _, cell, value = await document()
        outputs = cell.get("outputs").to_py()
        # Return only the two expected outputs, never arbitrary kernel data.
        output = next((o.get("text") for o in outputs if o.get("output_type") == "stream"
                       and o.get("text", "").strip() in {"12", "14"}), None)
        return {"notebook": NOTEBOOK, "cell_id": CELL, "source": source(value),
                "value": value, "output": output}


async def set_demo_value(value: Literal[6, 8], expected_value: Literal[6, 8]) -> dict:
    """Change only the last list value (6 or 8). Requires human approval. Does not execute code.

    First read_demo_cell; pass its current value as expected_value to reject stale edits.
    """
    if type(value) is not int or value not in (6, 8) or expected_value not in (6, 8):
        raise ValueError("Only 6 and 8 are supported.")
    async with LOCK:
        room, ydoc, cell, current = await document()
        if current != expected_value:
            raise ValueError("The cell changed after review. Read it and propose again.")
        await edit_cell(NOTEBOOK, CELL, content=source(value), animate=False)
        # JSD autosaves; the old output intentionally remains until execution.
        await asyncio.sleep(0)
        return {"changed": current != value, "value": value, "executed": False,
                "note": "Document changed through JSD. Kernel and old output are unchanged."}


async def run_demo_cell(expected_value: Literal[6, 8]) -> dict:
    """Execute the reviewed arithmetic cell through JSD in its existing notebook kernel.

    Requires human approval. First read_demo_cell and pass its current value.
    """
    async with LOCK:
        room, _, cell, value = await document()
        if value != expected_value:
            raise ValueError("The cell changed after review. Read it and propose again.")
        # The pinned JSD API rejects a source mismatch before queueing execution.
        await room.execute_cell(CELL, _source_hash(source(value)), clear_outputs=True)
        for _ in range(300):
            await asyncio.sleep(0.1)
            if cell.get("execution_state") == "idle":
                outputs = cell.get("outputs").to_py()
                expected = str(6 + value)
                if not any(o.get("output_type") == "stream" and
                           o.get("text", "").strip() == expected for o in outputs):
                    raise RuntimeError("The expected arithmetic output was not observed.")
                return {"executed": True, "output": expected, "value": value,
                        "note": "JSD updated the notebook output; the kernel now holds total."}
        raise TimeoutError("Kernel execution did not finish within 30 seconds.")

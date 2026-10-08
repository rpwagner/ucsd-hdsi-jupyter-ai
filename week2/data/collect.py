"""Recollect/resume the bounded public PR snapshot. Standard library only.

Run from anywhere: python week2/data/collect.py --resume
Without --resume, writes a separately dated directory; never overwrites evidence.
Uses public unauthenticated GitHub REST. Stops on API/rate-limit errors.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
REPOS = ['jupyterlab/jupyterlab', 'jupyter-server/jupyter_server', 'ipython/ipykernel']
WINDOW = 'created:2026-01-01..2026-10-07'


def project(item):
    user = item.get('user') or {}
    return dict(repository=item['repository_url'].split('/repos/')[1],
                number=item['number'], url=item['html_url'],
                created_at=item['created_at'], author_login=user.get('login'),
                author_id=user.get('id'), author_type=user.get('type'),
                merged_at=item.get('pull_request', {}).get('merged_at'))


def collect(out, kind, queries):
    meta_path = out / (kind + '-collection.json')
    raw_path = out / (kind + '-prs.jsonl')
    metadata = json.loads(meta_path.read_text()) if meta_path.exists() else []
    records = [json.loads(s) for s in raw_path.read_text().splitlines()] if raw_path.exists() else []
    last_request = 0
    for subject, query in queries:
        pages = [p for p in metadata if p['query'] == query]
        total = pages[0]['total_count'] if pages else None
        page = 1
        while total is None or page <= (total + 99) // 100:
            if any(p['page'] == page for p in pages):
                page += 1
                continue
            time.sleep(max(0, 8 - (time.monotonic() - last_request)))
            url = 'https://api.github.com/search/issues?' + urlencode(dict(q=query, sort='created', order='asc', per_page=100, page=page))
            last_request = time.monotonic()
            with urlopen(Request(url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'week2-eye-research'}), timeout=30) as response:
                payload = json.load(response)
            assert not payload['incomplete_results'], 'Incomplete API search'
            assert payload['total_count'] <= 1000, 'Partition query before collecting over 1000 results'
            assert total is None or total == payload['total_count'], 'Search population changed; use a fresh directory'
            total = payload['total_count']
            new = [project(x) for x in payload['items']]
            assert len(new) == len({x['url'] for x in new}), 'Duplicate records within page'
            assert not ({x['url'] for x in new} & {x['url'] for x in records}), 'Duplicate page records'
            records.extend(new)
            metadata.append(dict(**subject, query=query, url=url, page=page,
                                 total_count=total, returned_count=len(new),
                                 incomplete_results=payload['incomplete_results'],
                                 collected_at=datetime.now(timezone.utc).isoformat()))
            raw_path.write_text(''.join(json.dumps(r) + '\n' for r in records))
            meta_path.write_text(json.dumps(metadata, indent=2) + '\n')
            print(subject, page, len(new), total, flush=True)
            page += 1
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    out = ROOT if args.resume else ROOT / ('rerun-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    out.mkdir(parents=True, exist_ok=True)
    collect(out, 'component', [({'repo': repo}, f'is:pr repo:{repo} {WINDOW}') for repo in REPOS])
    logins = json.loads((ROOT / 'collection-logins.json').read_text())
    collect(out, 'person', [({'login': login}, f'is:pr is:public author:{login} {WINDOW}') for login in logins])

"""Reproduce the bounded Week 3 research tables and figure offline (stdlib).

Classification is a human evidence judgement. Validation checks its references,
dates and arithmetic; it cannot prove that an origin search was exhaustive.
SVG helpers adapt week2/data/analyze.py, retaining the blue/purple layout.
"""
from collections import Counter, defaultdict
import csv
from datetime import datetime
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CUTOFF = '2026-10-15T00:00:00Z'
CODE_SETTINGS = {
    'official_jupyter_repository': 'Official Jupyter repository',
    'personal_repository': 'Personal repository',
    'company_repository': 'Company repository',
    'jupyter_ai_contrib_repository': 'jupyter-ai-contrib repository',
    'unresolved': 'Initial setting unresolved',
}
PEOPLE_INVOLVEMENT = {
    'prior_contribution_documented': 'Prior contribution documented',
    'history_unknown': 'Prior history unknown',
    'documented_newcomer': 'Newcomer status documented',
    'mixed_backgrounds': 'Mixed backgrounds documented',
}


def read(name):
    return json.loads((ROOT / name).read_text())


def write_csv(name, rows):
    with (ROOT / name).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def text(svg, x, y, value, size=22, bold=False):
    svg.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
               f'font-size="{size}" font-weight="{700 if bold else 400}" '
               f'fill="#17243C">{escape(str(value))}</text>')


def main():
    projects = read('inventory.json')
    people = read('people-evidence.json')
    sources = read('source-index.json')
    milestones = read('milestones.json')
    relations = read('relationships.json')
    by_id = {p['id']: p for p in projects}
    assert len(by_id) == len(projects), 'Duplicate project'
    assert len({s['id'] for s in sources}) == len(sources), 'Duplicate source'
    witnesses = {p['login'].lower(): p for p in people if p['evidence_kind'] == 'merged_pr'}
    known_urls = set()
    for source in sources:
        assert source['collected_at'].endswith('Z')
        record = source['record']
        known_urls.add(source['request_url'])
        if isinstance(record, list):
            known_urls.update(r['html_url'] for r in record)
        elif record.get('url'):
            known_urls.add(record['url'])
        if isinstance(record, dict):
            known_urls.update(r['url'] for r in record.get('sources', []))
    categories = Counter()
    years = Counter()
    accounts = defaultdict(set)
    for project in projects:
        assert project['initial_code_setting'] in CODE_SETTINGS
        assert project['prior_jupyter_involvement'] in PEOPLE_INVOLVEMENT
        assert project['software_lineage'], 'Missing separate software lineage'
        datetime.strptime(project['first_evidence_date'], '%Y-%m-%d')
        assert project['first_evidence_date'] < CUTOFF[:10]
        assert project['first_evidence_url'] in known_urls, project['id']
        assert project['snapshot_commit_author_date'] < CUTOFF
        positive = []
        for login in project['origin_accounts']:
            accounts[login.lower()].add(project['id'])
            if login.lower() in witnesses:
                witness = witnesses[login.lower()]
                # A PR opened earlier but merged later would not pass this check.
                assert witness['merged_at'][:10] < project['first_evidence_date']
                positive.append(login)
        if project['prior_jupyter_involvement'] == 'prior_contribution_documented':
            assert positive, f'No prior dated witness: {project["id"]}'
        elif project['prior_jupyter_involvement'] == 'history_unknown':
            assert not positive, 'Resolve contradictory classification'
        else:
            raise AssertionError('Newcomer/mixed classifications require an additional evidence audit')
        categories[(project['initial_code_setting'], project['prior_jupyter_involvement'])] += 1
        years[project['first_evidence_date'][:4]] += 1
    for event in milestones:
        assert event['project'] in by_id
        assert event['date'] < CUTOFF[:10]
        assert event['url'] in known_urls, event['url']
    for edge in relations:
        assert edge['source'] in by_id and edge['target'] in by_id
        assert edge['evidence_id'] in {s['id'] for s in sources}
    shared = [dict(login=login, case_count=len(ids), cases=';'.join(sorted(ids)))
              for login, ids in accounts.items() if len(ids) > 1]
    shared.sort(key=lambda row: (-row['case_count'], row['login']))
    code_counts = Counter(p['initial_code_setting'] for p in projects)
    people_counts = Counter(p['prior_jupyter_involvement'] for p in projects)
    summary = dict(cutoff_exclusive_utc=CUTOFF, projects=len(projects),
                   initial_code_setting_counts=dict(code_counts),
                   prior_jupyter_involvement_counts=dict(people_counts),
                   classification_cross_tab=[dict(initial_code_setting=setting,
                                                   prior_jupyter_involvement=involvement,
                                                   count=categories[(setting, involvement)])
                                             for setting in CODE_SETTINGS
                                             for involvement in PEOPLE_INVOLVEMENT],
                   evidence_year_counts=dict(sorted(years.items())),
                   projects_with_prior_contributor=people_counts['prior_contribution_documented'],
                   projects_with_unknown_prior_involvement=people_counts['history_unknown'],
                   retained_relationships=len(relations), shared_origin_accounts=shared)
    (ROOT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    rows = [dict(project=p['project'], date=p['first_evidence_date'],
                 event_kind=p['first_evidence_kind'], finding=p['capability'], url=p['first_evidence_url'])
            for p in projects]
    rows += [dict(project=by_id[e['project']]['project'], date=e['date'],
                  event_kind=e['event_kind'], finding=e['finding'], url=e['url']) for e in milestones]
    rows.sort(key=lambda r: (r['date'], r['project'], r['event_kind']))
    write_csv('timeline.csv', rows)
    write_csv('shared-origin-accounts.csv', shared)
    write_csv('project-classifications.csv', [
        dict(project=p['project'], initial_code_setting=CODE_SETTINGS[p['initial_code_setting']],
             prior_jupyter_involvement=PEOPLE_INVOLVEMENT[p['prior_jupyter_involvement']],
             software_lineage=p['software_lineage'], setting_evidence=p['setting_evidence_note'],
             early_accounts=';'.join(p['origin_accounts']),
             evidence_urls=';'.join(p['evidence_urls'])) for p in projects])
    # Two independent dimensions; no insider/outsider identity classification.
    # Not a prevalence estimate: individual components and whole projects coexist.
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="730" '
           'viewBox="0 0 1100 730" role="img" aria-labelledby="title desc">',
           '<title id="title">Code setting and people\'s prior Jupyter involvement</title>',
           '<desc id="desc">Twelve cases, shown by initial repository setting and separately '
           'by prior contributor evidence: official Jupyter 1 documented, 0 unknown; personal '
           '5 documented, 2 unknown; company 1 documented, 0 unknown; jupyter-ai-contrib '
           '2 documented, 0 unknown; unresolved setting 1 documented, 0 unknown.</desc>',
           '<rect width="1100" height="730" fill="#FFFFFF"/>']
    text(svg, 45, 55, "Code setting and people's prior involvement", 34, True)
    text(svg, 45, 94, '12 case histories | evidence through October 14, 2026 UTC', 22)
    text(svg, 45, 161, 'Initial code setting', 23, True)
    text(svg, 540, 144, 'Prior contribution', 22, True)
    text(svg, 540, 173, 'documented', 21)
    text(svg, 815, 144, 'Prior history', 22, True)
    text(svg, 815, 173, 'unknown', 21)
    for index, (setting, label) in enumerate(CODE_SETTINGS.items()):
        y = 230 + index * 65
        text(svg, 45, y, label, 23, True)
        for x, involvement, color in [(540, 'prior_contribution_documented', '#2667DA'),
                                      (815, 'history_unknown', '#6953BD')]:
            n = categories[(setting, involvement)]
            svg.append(f'<rect x="{x}" y="{y-31}" width="220" height="45" rx="7" fill="#EBEEF4"/>')
            svg.append(f'<text x="{x+110}" y="{y}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
                       f'font-size="28" font-weight="700" fill="{color}">{n}</text>')
    text(svg, 45, 569, 'Documented = at least one early account with a Jupyter/IPython PR merged', 20)
    text(svg, 45, 600, 'before the effort. Repository setting says nothing about a person\'s membership.', 20)
    text(svg, 45, 639, 'Counts total 12; unknown history is not newcomer status. Software lineage is separate.', 19)
    text(svg, 45, 670, 'Purposive inventory; related components count separately. No adoption measure.', 19)
    text(svg, 45, 701, 'Sources: dated PRs and pinned code. See week3/research.md and data/.', 19)
    svg.append('</svg>')
    images = ROOT.parent / 'images'
    images.mkdir(exist_ok=True)
    (images / 'origin-inventory.svg').write_text('\n'.join(svg) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()

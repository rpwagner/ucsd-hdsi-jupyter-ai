"""Reproduce Week 2 tables and SVGs offline from retained records (stdlib only)."""
from collections import Counter, defaultdict
import csv
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT.parent / 'images'
START, END = '2026-01-01T00:00:00Z', '2026-10-08T00:00:00Z'
REPOS = ['jupyterlab/jupyterlab', 'jupyter-server/jupyter_server', 'ipython/ipykernel']


def read_json(name):
    return json.loads((ROOT / name).read_text())


def read_records(kind):
    records = [json.loads(s) for s in (ROOT / (kind + '-prs.jsonl')).read_text().splitlines()]
    assert len(records) == len({r['url'] for r in records}), f'Duplicate {kind} records'
    assert all(START <= r['created_at'] < END for r in records), 'Out-of-window PR'
    metadata = read_json(kind + '-collection.json')
    assert all(p['incomplete_results'] is False for p in metadata), 'Incomplete API search'
    by_query = defaultdict(list)
    for p in metadata:
        by_query[p['query']].append(p)
    for query, pages in by_query.items():
        totals = {p['total_count'] for p in pages}
        assert len(totals) == 1 and max(totals) <= 1000
        total = next(iter(totals))
        assert sorted(p['page'] for p in pages) == list(range(1, max(1, (total + 99) // 100) + 1)), f'Incomplete query: {query}'
        assert sum(p['returned_count'] for p in pages) == total
    assert sum(p['returned_count'] for p in metadata) == len(records)
    return records


def excluded(r):
    login = (r['author_login'] or '').lower()
    if not login:
        return 'missing_author'
    if r['author_type'] == 'Bot' or login.endswith('[bot]'):
        return 'bot_type_or_suffix'
    if login == 'meeseeksmachine':
        return 'documented_machine_account'
    return ''


def write_csv(name, rows, fields):
    with (ROOT / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def svg_start(title, desc, height):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" viewBox="0 0 1100 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
            f'<rect width="1100" height="{height}" fill="#FFFFFF"/>']


def text(svg, x, y, value, size=22, bold=False):
    svg.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="#17243C">{escape(str(value))}</text>')


def main():
    components = read_records('component')
    raw_people = read_records('person')
    leadership = read_json('leadership-roster.json')
    leaders = {p['login'].lower() for p in leadership}
    selected = set()
    selection_rows, component_summary = [], []
    for repo in REPOS:
        raw = [r for r in components if r['repository'] == repo]
        kept = [r for r in raw if not excluded(r)]
        counts = Counter(r['author_login'].lower() for r in kept)
        cutoff = sorted(counts.values(), reverse=True)[4]
        for rank, (login, count) in enumerate(sorted(counts.items(), key=lambda t: (-t[1], t[0])), 1):
            is_selected = count >= cutoff
            selection_rows.append(dict(repository=repo,rank=rank,login=login,pr_count=count,selected=is_selected,cutoff_prs=cutoff))
            if is_selected:
                selected.add(login)
        component_summary.append(dict(repository=repo,all_prs=len(raw),excluded_prs=len(raw)-len(kept),retained_prs=len(kept),account_count=len(counts),cutoff_prs=cutoff))
    population = leaders | selected
    assert population == set(read_json('collection-logins.json'))
    meta_logins = {p['login'] for p in read_json('person-collection.json')}
    assert meta_logins == population
    # GitHub author searches can return delegated/coauthored submissions with a
    # different recorded opening account. Keep the response, but do not reassign.
    people = [r for r in raw_people if (r['author_login'] or '').lower() in population and not excluded(r)]
    mismatch = [r for r in raw_people if r not in people]
    counts = Counter((r['author_login'].lower(), r['repository']) for r in people)
    qualifying_repos = {repo for (_, repo), n in counts.items() if n >= 3}
    registry = {p['repository']: p for p in read_json('project-registry.json')}
    assert qualifying_repos <= registry.keys(), f'Missing classifications: {qualifying_repos - registry.keys()}'
    edges = []
    for (login, repo), n in sorted(counts.items()):
        if n < 3:
            continue
        info = registry[repo]
        evidence = [r for r in people if r['author_login'].lower() == login and r['repository'] == repo]
        edges.append(dict(login=login,project=info['project'],repository=repo,category=info['category'],status=info['status'],evidence_type='recent_pr_activity',pr_count=n,
                          merged_by_cutoff=sum(bool(r['merged_at']) and r['merged_at'] < END for r in evidence),evidence_urls=';'.join(r['url'] for r in evidence)))
    accepted = [e for e in edges if e['status'] == 'included']
    # Threshold is at repository level; projects group repositories only after
    # qualification. A person is counted once per project or population.
    summary = dict(window_start_utc=START,window_end_exclusive_utc=END,
                   component_total=len(components),component_excluded=sum(bool(excluded(r)) for r in components),
                   component_retained=sum(not excluded(r) for r in components),
                   component_accounts=len({r['author_login'].lower() for r in components if not excluded(r)}),
                   selected_accounts=len(selected),leadership_people=len(leaders),population_union=len(population),population_intersection=len(leaders & selected),
                   person_search_records=len(raw_people),person_records_used=len(people),person_records_excluded=len(mismatch),
                   component_selected_prs=sum(r['author_login'].lower() in selected for r in components if not excluded(r)))
    person_rows = []
    role_evidence = read_json('role-evidence.json')
    for login in sorted(population):
        row = dict(login=login,leadership=login in leaders,key_contributor=login in selected)
        for category in ['official_jupyter','adjacent_jupyter','non_jupyter']:
            row[category + '_projects'] = ';'.join(sorted({e['project'] for e in accepted if e['login'] == login and e['category'] == category}))
        row['non_jupyter_roles'] = ';'.join(sorted({e['project'] for e in role_evidence if e['login'] == login and e['in_population']}))
        row['unclassified_or_excluded_repositories'] = ';'.join(e['repository'] for e in edges if e['login'] == login and e['status'] != 'included')
        row['interpretation'] = 'Documented matches only; blank fields do not establish absence of relationships'
        person_rows.append(row)
    for label, cohort in [('leadership',leaders),('key_contributors',selected)]:
        for category in ['official_jupyter','adjacent_jupyter','non_jupyter']:
            summary[label + '_' + category + '_recent'] = len({e['login'] for e in accepted if e['login'] in cohort and e['category'] == category})
        roles = {e['login'] for e in role_evidence if e['in_population'] and e['login'] in cohort}
        summary[label + '_documented_roles'] = len(roles)
        summary[label + '_non_jupyter_either'] = len(roles | {e['login'] for e in accepted if e['login'] in cohort and e['category'] == 'non_jupyter'})
    project_rows = []
    for project in sorted({e['project'] for e in accepted if e['category'] == 'non_jupyter'}):
        prs = {e['login'] for e in accepted if e['project'] == project}
        roles = {e['login'] for e in role_evidence if e['project'] == project and e['in_population']}
        project_rows.append(dict(project=project,recent_people=len(prs),recent_leaders=len(prs & leaders),recent_key_contributors=len(prs & selected),recent_logins=';'.join(sorted(prs)),role_logins=';'.join(sorted(roles))))
    project_rows.sort(key=lambda r:(-r['recent_people'],r['project']))
    summary['non_jupyter_recent_projects'] = len(project_rows)
    summary['non_jupyter_recent_edges'] = sum(e['category']=='non_jupyter' for e in accepted)
    write_csv('component-authors.csv', selection_rows, ['repository','rank','login','pr_count','selected','cutoff_prs'])
    write_csv('component-summary.csv', component_summary, list(component_summary[0]))
    write_csv('people-summary.csv', person_rows, list(person_rows[0]))
    write_csv('recent-edges.csv', edges, list(edges[0]))
    write_csv('external-project-summary.csv', project_rows, list(project_rows[0]))
    write_csv('excluded-search-records.csv', mismatch, list(raw_people[0]))
    (ROOT / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    IMAGES.mkdir(exist_ok=True)
    svg = svg_start('Documented non-Jupyter PR connections', 'Accounts with at least three 2026 PR submissions to a qualifying non-Jupyter repository; measured in overlapping, nonrepresentative populations.', 510)
    text(svg,45,58,'Documented non-Jupyter PR connections',36,True)
    text(svg,45,98,'2026-01-01 through 2026-10-07 UTC | distinct accounts in each population',22)
    for y,label,prefix,total,color in [(180,'Current leadership','leadership',len(leaders),'#2667DA'),(295,'Component contributors','key_contributors',len(selected),'#6953BD')]:
        n=summary[prefix+'_non_jupyter_recent']
        text(svg,45,y,label,24,True)
        svg.append(f'<rect x="365" y="{y-32}" width="455" height="44" rx="8" fill="#EBEEF4"/>')
        svg.append(f'<rect x="365" y="{y-32}" width="{455*n/total:.2f}" height="44" rx="8" fill="{color}"/>')
        text(svg,850,y,f'{n} / {total}',28,True)
        text(svg,850,y+30,f'{100*n/total:.1f}%',21)
    text(svg,45,382,'At least 3 opened PRs per repository; licenses and project boundaries checked.',21)
    text(svg,45,416,'The groups overlap: 4 accounts are in both. Unclassified is not “no overlap”.',21)
    text(svg,45,450,'Submitted activity ≠ effort, influence or accepted work. Roles are separate evidence.',20)
    text(svg,45,484,'Sources: retained public GitHub PR records; governance roster. See research.md.',19)
    svg.append('</svg>');(IMAGES/'population-overlap.svg').write_text('\n'.join(svg)+'\n')
    top=project_rows[:5]
    height=220+len(top)*74
    svg=svg_start('Where multiple sampled accounts connect', 'Five non-Jupyter projects with the most distinct qualifying PR-opening accounts in the union of both populations. Roles are not included in these bars.',height)
    text(svg,45,58,'Where multiple sampled accounts connect',35,True)
    text(svg,45,96,'Distinct accounts with qualifying 2026 PR activity | union of both populations',21)
    maximum=max(r['recent_people'] for r in top)
    for i,row in enumerate(top):
        y=160+i*74
        text(svg,45,y,row['project'],24,True)
        svg.append(f'<rect x="420" y="{y-30}" width="420" height="40" rx="8" fill="#EBEEF4"/>')
        svg.append(f'<rect x="420" y="{y-30}" width="{420*row["recent_people"]/maximum:.2f}" height="40" rx="8" fill="#2667DA"/>')
        text(svg,870,y,f'{row["recent_people"]} accounts',23,True)
    text(svg,45,height-84,'Projects group related repositories after the 3-PR threshold is applied per repository.',20)
    text(svg,45,height-51,'Ties ordered alphabetically. One person counted once per project; no role edges added.',19)
    text(svg,45,height-18,'2026-01-01 through 2026-10-07 UTC. Sources and all edges: data/ and research.md.',19)
    svg.append('</svg>');(IMAGES/'shared-projects.svg').write_text('\n'.join(svg)+'\n')
    print(json.dumps(summary,indent=2))
    print('Top external projects:', project_rows[:8])


if __name__ == '__main__':
    main()

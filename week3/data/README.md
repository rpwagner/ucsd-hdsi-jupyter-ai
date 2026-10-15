# Week 3 research data

**Twelve selected histories; cutoff exclusive 2026-10-15T00:00:00Z.** Collection
occurred October 15 UTC / October 15 Pacific. This directory supports
[research.md](../research.md), not a contributor census or an adoption measure.
It is public-source research awaiting publication approval.

## Reproduce offline

From the repository root, using Python 3.10 or later:

```sh
python week3/data/analyze.py
```

Python's standard library is sufficient. No package installation, network access,
model query or credential is needed. This regenerates `summary.json`,
`timeline.csv`, `shared-origin-accounts.csv`, `project-classifications.csv` and
`../images/origin-inventory.svg`.
The script validates identifiers, known source URLs, relationship endpoints,
date formats, cutoff bounds, and a prior **merge**, not just an earlier PR opening,
for every positive project classification. These checks do not automate judgement
about historical origins or establish that the research is exhaustive.

The CSV/SVG helpers adapt `week2/data/analyze.py`. Week 1's classifications are
background leads, not evidence imported as newly verified. Earlier research and
data are unchanged. The existing SVG palette/layout is reused; no logo is needed
for this research-stage figure.

## Inputs and outputs

| File | Role |
| --- | --- |
| `selection.md` | Inclusion rule, fixed population, excluded/contextual projects and exact discovery queries |
| `inventory.json` | Twelve human-audited cases: first evidence, separate initial code setting and prior Jupyter involvement, software lineage, current home, early accounts, pinned cutoff commit and source links |
| `people-evidence.json` | Prior merged-PR witnesses, narrowly bounded unsuccessful searches and unresolved accounts; no identity matching by names or email |
| `milestones.json` | Selected subsequent proposals, renames, implementations and releases; event kinds remain separate |
| `relationships.json` | Seven selected reuse links; direct required dependencies, an optional extra and a documented tool path are distinguished |
| `source-index.json` | Public-safe source identifiers, exact request URLs, collection times and event kinds used by the offline calculations; no third-party body-text snapshots |
| `collection.json` | Source count, hashes, project-main starting revision, cutoffs and collection interval |
| `summary.json` | Generated counts; no rounding or percentages |
| `project-classifications.csv` | Generated readable per-project table with independent code setting, people's prior involvement, software lineage and evidence |
| `timeline.csv` | Generated first-evidence and subsequent-event chronology, with primary links |
| `shared-origin-accounts.csv` | Generated recurring early-role accounts in this population; not a founder/maintainer census |
| `analyze.py` | Offline checks, calculations and SVG generation |

`initial_code_setting` describes **only the code's initial organizational setting**:
`official_jupyter_repository`, `personal_repository`, `company_repository`,
`jupyter_ai_contrib_repository`, or `unresolved`. Historical README links provide
positive original-namespace evidence. Present ownership is never projected backward.
The contrib category identifies a repository namespace, not independent official
subproject status. Personal/company/contrib hosting says nothing about whether
the people are longstanding Jupyter leaders, contributors or newcomers.

`prior_jupyter_involvement` describes **the people's prior involvement evidence**:
`prior_contribution_documented` requires **at least one** attributed early account
with a public Jupyter/IPython PR merged before inception evidence. It is not a
measure of seniority, membership or a team's mandate. `history_unknown` means not
established. `documented_newcomer` and `mixed_backgrounds` require affirmative
dated evidence, are unused here, and the analysis refuses to accept them without
an additional evidence audit. Unknown history never establishes newcomer status.
A known prior contributor alongside another account with unknown history still
supports only the at-least-one result, not a documented mixed-background label.
Dated leadership could supply another kind of evidence in a later audit; this
snapshot's systematic witness rule remains prior merged contributions.

`software_lineage` independently retains the evidence narrative: new Jupyter
implementation, external-software adaptation/fork, model/protocol integration,
or extraction of existing code. These descriptions can coexist. An extracted
Jupyter component in contrib has a different code lineage from a personal
experiment adapting external software, even when both involve prior contributors.
No single inside/outside category combines these dimensions. The earlier schema's
`initial_setting`, `people_origin` and `software_provenance` fields are replaced,
with the evidence records and collection cutoff preserved.

`origin_accounts` are selected attributable early roles. In particular: Jupyter
AI's January precursor is attributed to `3coins`; launch and subsequent leadership
are separate evidence. JSD and Server MCP explicitly distinguish repository
bootstraps from implementation and merge roles. Datalayer distinguishes `echarles`
initialization from `eleonorecharles` implementation, without merging identities.
One subsequently verified contributor (`brichet`) is in people evidence but not
an origin account. Logins are not proof of human authorship or distinct people.

## Collection method and limits

The GitHub connector read public repository metadata, commit pages, pinned files,
specific issues/PRs and releases. Each `source-index.json` entry retains the source ID, exact `request_url`,
actual UTC `collected_at`, record type, and selected evidence URLs. File URLs
encode the repository, commit `ref` and path passed to `fetch_file`; API
request URLs retain exact parameters. The full collected file/PR body snapshots
remain in the private working archive and are not redistributed here. No administrative membership or private source project was accessed.
The private destination repository supplied only project instructions/context.

For each selected repository:

1. Read repository metadata (creation date is a locator, not the start date).
2. Read `commits?until=<creation plus seven days>&per_page=100` to locate early
   attributable work and imported history. Retained pages are bounded windows,
   **not full repository histories**. PR #13804's commit page verifies its sole
   January precursor commit. Jflam's inherited Google-extension commits are
   retained but excluded as Jupyter origins.
3. Read `commits?until=2026-10-15T00:00:00Z&per_page=1` and pin relevant README,
   dependency and release-note files to that returned commit. Author and committer
   dates are retained; these are code snapshots, not assertions about released
   package versions. Branch history rewritten after collection could change results.
4. Inspect named decisions, releases and implementation records. Release metadata
   observes `published_at`; proposals are not silently treated as releases.
5. For prior contribution, search targeted public Jupyter repositories with an
   explicit pre-origin date, `sort=created&order=asc&per_page=3&page=1`; retain the
   query, total, `incomplete_results` and witness records. Inspect specific positive
   PRs to establish author and merge time. All retained searches report
   `incomplete_results=false`. **Only three hits are retained**, not all hits;
   search totals are never used as activity metrics. Two zero-result searches are
   limited to `org:jupyterlab` and cannot prove no prior community relationship.

For fresh checks, replay the public source-index requests into a **new dated
directory**, re-audit classifications and do not overwrite this historical record.
Public records can change, disappear or transfer. File/commit pins improve
inspectability but neither GitHub Search nor the collection is an atomic snapshot.
Web primary-page observations retain source/title/date and a short observation;
they are not complete archival captures. Discovery search snippets are not retained
as proof of affiliation or provenance. All factual classification evidence is
available in code/PR records; the web launch posts add dated announcement context.

The publicly shared source index deliberately omits collected third-party
README text, issue/PR bodies and commit patches. It allows reproducible URL,
evidence-ID and date checks and regeneration of the published counts, tables and
SVG, but it is not a verbatim archive of external sources. The original collection
contained public project history only; no private credentials were collected.
The original collection hash of the private source archive remains in
`collection.json` as provenance, not as a hash of this public projection.

## Interpretation and grouping

The first-evidence year bins mix explicitly labeled event kinds and do not measure
ecosystem growth. Related components count separately: collapsing Jupyter AI,
JSD, Server MCP, Persona Manager, AI Commands and ACP Client into one family
reduces twelve rows to seven cases. Source selection favors existing Jupyter
connections and the prepared Week 3 map. Do not generalize 10/12 to all AI software
around Jupyter or to a share of contributors. No PR totals, download totals, user
population, governance prevalence, effort or motives are measured.

The SVG cross-tabulates code setting against prior-involvement evidence, with
separate marginals and all reserved-category zero counts in `summary.json`.
It was rendered with Sharp and inspected at 1100 × 730 pixels. The PNG is a
local QA intermediate, not a committed research deliverable. Labels, counts,
source pointer and cautions are visible within the margins.

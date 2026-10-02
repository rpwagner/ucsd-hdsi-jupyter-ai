# Week 1 data guide

**Reporting snapshot: 2026-09-30. Documentation audit: 2026-10-01.**

These files preserve an exploratory GitHub activity aggregation, not a complete census or a survey of AI opinions. No new contributor collection was performed for this revision.

## Retained files

| File | Meaning | Status |
| --- | --- | --- |
| [Summary](ai-space-pr-summary-2026.csv) | Original aggregate metrics | Values retained unchanged; full PR-level population is unavailable |
| [Top 60 accounts](ai-space-pr-authors-top60-2026.csv) | GitHub login, PR count, semicolon-separated repository set | 60 rows totaling 697 PRs; original aggregation reported 63 accounts and 700 PRs |
| [Top 20 overlap](top20-official-jupyter-overlap-2026.csv) | Original manual classification and explanatory notes | Provisional: no direct per-account evidence URL was retained for every classification |
| [Policy snapshot](ai-policy-snapshot-2026-09-30.csv) | Sources classified as policy, practice, experiment or discussion | Evidence periods and limits now explicit |

The first three CSVs retain their historical bytes, names and field labels so a wording correction cannot masquerade as a new collection.

## Interpret the legacy labels correctly

`human_prs` means PRs opened by accounts not identified as bots under the original filter (GitHub user type `Bot` or a login ending in `[bot]`). `unique_human_authors` means distinct account logins after that filter. Neither establishes that the submitted code/text was human-authored, that an account had no automation, or that every login is a unique person.

In the overlap file, `yes` means the original analyst marked an account as overlapping. The notes are not a complete evidence audit. `not-established-in-this-pass` means unknown, not no history, not new to Jupyter and not opposition to AI. The metric names beginning `conservative_overlap_` are historical labels; treat the resulting percentage as provisional, not a verified statistical lower bound.

## Checks possible from the retained records

The account table sums to 697. Its top 5, 10 and 20 rows sum to 472, 571 and 645. Dividing those by the original recorded denominator of 700 gives 67.4%, 81.6% and 92.1%, rounded to one decimal place. These are cumulative groups, not separate slices to add together.

The 10 rows flagged `yes` in the overlap table sum to 522 PRs. `522 / 700 * 100 = 74.6%`. This checks arithmetic, not the underlying classification. The remaining 178 PRs are outside that flagged set; they are not proven to be from people outside Jupyter.

The summary reports three omitted one-PR accounts. Their identities and individual PR records were not retained and have not been reconstructed. Opened PRs are counted, not only merged PRs. No effort, review burden or policy-opinion measure was collected.

## Original scope and collection gaps

The aggregation queried PRs opened in 2026 in `jupyterlab/jupyter-ai`, `jupyterlite/ai`, and `jupyter-ai-contrib`. Public subproject/governance pages were a proxy for official-Jupyter scope, not an exported GitHub Enterprise organization roster. Being in an AI repository that is itself official was not intended, by itself, to prove non-AI cross-project history.

The visible original queries were `is:pr org:jupyter-ai-contrib created:>=2026-01-01`, `is:pr repo:jupyterlab/jupyter-ai created:>=2026-01-01`, and `is:pr repo:jupyterlite/ai created:>=2026-01-01`, paginated at 100 results and sorted by creation date. They did not encode an upper cutoff. The September 30 label is the analyst's reporting snapshot, not a fully retained UTC extraction contract. Do not silently invent exact cutoff times or claim the saved aggregates fully reproduce the API response.

Before a future rerun, record an explicit start and end time with timezone, repository roster, bot rule, query strings, pagination/completeness checks, PR URL and author ID for every record, and evidence URL/date for each overlap classification. Keep public history evidence separate from membership and governance roles. Date the rerun separately; do not overwrite this snapshot as though missing records had been recovered.

Raw participant observations and survey responses must never be placed here. This directory is for vetted public-source research data eligible for later publication.

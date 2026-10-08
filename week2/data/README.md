# Week 2 data guide

**Snapshot: PRs opened 2026-01-01T00:00:00Z through 2026-10-07T23:59:59Z. Sources collected 2026-10-08 UTC / 2026-10-07 Pacific.**

Public-source evidence for [research](../research.md) and [The Eye](../the-eye.md). No participant observations, private repository activity, credentials, emails or private membership data are included. This is a new collection, not a replacement for Week 1's exploratory snapshot.

## Reproduce the retained analysis

From the repository root, with Python 3.10 or later:

```bash
python week2/data/analyze.py
```

Standard library only; no network, model call or optional plotting dependency. It regenerates the six CSV tables below, `summary.json`, and both SVGs in `../images/`. The outputs use sorted logins and deterministic tie ordering. It checks unique PR URLs, creation bounds, complete page sequences, stable totals, required population queries and a classification for every repository reaching the activity threshold. A failed assertion stops reproduction.

For a **fresh public collection**, preserving this snapshot:

```bash
python week2/data/collect.py
```

The collector writes a new `rerun-<UTC timestamp>/` directory. It uses the fixed opening window and the saved 32-login population; it does not refresh governance membership or manually classify new projects. Copy the retained analysis script and classification inputs into that separate directory only after auditing differences. GitHub metadata and search indexing can change, so a new extraction need not match these bytes. The collector stops on HTTP/rate-limit errors, incomplete results, changed counts, duplicate pages or a query exceeding 1,000 results. `--resume` resumes the dated files alongside the script; do not use it to silently change this historical snapshot. No credentials are required.

## Inputs and outputs

| File | Role |
| --- | --- |
| `component-prs.jsonl` | Projected API records for all 1,050 component PRs, including excluded accounts |
| `component-collection.json` | Eleven component pages: exact queries/URLs, totals, page sizes and collection timestamps |
| `person-prs.jsonl` | Projected API records for all 6,155 public-author-search results |
| `person-collection.json` | Eighty-two person pages, including zero-result queries and extraction metadata |
| `collection-logins.json` | Frozen union of the 24 roster logins and 12 selected contributor logins, deduplicated to 32 |
| `sources/jupyter-contributors.yml` | Upstream CC0 governance source; current and former memberships retained distinctly |
| `leadership-roster.json` | Current Foundation/SSC union with direct name/login mappings and roles |
| `source-records.json` | What was checked, when, and source blob IDs where available |
| `repository-metadata.json` | Public fork/license metadata and descriptions for 213 non-official candidates |
| `project-registry.json` | Manual classification and status for all 305 qualifying repositories, with sources and caveats |
| `role-evidence.json` | Explicit role evidence, dates, scope and the opening example's exclusion from denominators |
| `component-authors.csv` | Complete account rankings in each component, fifth-place cutoffs and selection flags |
| `component-summary.csv` | Raw/excluded/retained repository denominators |
| `people-summary.csv` | Every member of both populations, with documented category matches and unknown/excluded records |
| `recent-edges.csv` | All qualifying person/repository pairs, counts, category/status and every direct PR URL |
| `external-project-summary.csv` | Included non-Jupyter projects ranked by distinct qualifying accounts; role matches in a separate column |
| `excluded-search-records.csv` | Thirty Copilot-opening-account results excluded from person attribution |
| `summary.json` | Calculations used by article, research and charts |
| `collect.py` / `analyze.py` | Episode-specific collection/reproduction helpers |

Raw records are JSON Lines. The fields are `repository`, `number`, `url`, `created_at`, `author_login`, `author_id`, `author_type`, `merged_at`. A missing merge time is JSON `null`; it is not evidence about effort or impact. These fields preserve submitted PR activity and a merge observation without retaining entire copyrighted PR bodies or arbitrary profile content. Individual PRs remain inspectable at their URLs.

## Definitions

- Bot filter: GitHub `Bot`, login suffix `[bot]`, or the explicitly documented `meeseeksmachine` backport account. Excluded records remain in raw data. No filter proves the remaining submissions were human-authored.
- Key contributors: top five accounts **in each** component by retained PR count, including all ties at fifth place, then deduplicate. The rule is independent of external-project results.
- Recent edge: at least three PRs **opened by the recorded account in one repository**, in the fixed window. Count open and closed submissions. Do not credit a searched person when the record's opening account differs.
- Project grouping: applied **after** repository-level qualification. Group conda-forge, emscripten-forge and xtensor repositories within each family; keep unrelated company repositories separate. One account is counted once per project. Count conda-forge work as packaging, not upstream code in the packaged project.
- Categories: `official_jupyter`, `adjacent_jupyter`, `non_jupyter`. Official boundaries use the public governance roster proxy; adjacent means external Jupyter extensions/deployments/integrations, not every dependency Jupyter uses.
- Status: `included`, `excluded_fork`, `excluded_ancillary`, `excluded_source_available`, or `unclassified_license`. Neither exclusion nor an empty summary field proves absence of external participation. Fork exclusion is conservative and can exclude independently maintained forks.
- Roles: explicit published governance/core-team/maintainer evidence, recorded separately from recent PRs. The supplementary role audit is limited, with dated recognition labeled as such. Brian Granger is outside the measured population; his current PyTorch board role is the article's verified opening example.

## Arithmetic and chart conventions

The component tables contain 801 retained PRs from 195 unique case-normalized account logins. The selected 12 opened 446 of those PRs: `446 / 801 * 100 = 55.7%`. Leadership and contributor populations overlap by four accounts; their union is 32.

Qualifying recent non-Jupyter activity: `11 / 24 * 100 = 45.8%` and `10 / 12 * 100 = 83.3%`. These are documented-match rates under a bounded operational rule, not estimates of Jupyter-wide contribution or influence. Adding the limited role evidence produces 12/24 and 10/12 matches; do not add the role and activity rows.

The project-ranking chart counts qualifying PR-opening accounts only, in the population union. conda-forge has four; emscripten-forge three; PyData Sphinx Theme, Pyflyby and QuantStack/git2cpp two each. The other 89 included non-Jupyter projects each have one. Leadership and contributor columns in the project table overlap and must not be added. Role columns do not change PR-activity rankings.

The SVGs adapt Week 1's bar layouts and palette. Titles/descriptions, article alt text, dates, sources, denominators and caveats travel with each chart. Both were rendered and visually inspected at their native 1,100-pixel screen-sharing width before review. The approved Eye logo is referenced from the existing shared asset rather than duplicated or redesigned.

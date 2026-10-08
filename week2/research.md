# Week 2 research: people who connect open-source projects

**Reporting window ends October 7, 2026 UTC. Collection and source checks: October 8 UTC, during the evening of October 7 Pacific.**

Evidence record for [The Eye](the-eye.md). This implements the bounded question in #17 and #8: how do current Jupyter governance leaders and key contributors in the Week 2 component sample connect to other open-source projects? It is not a census of Jupyter contributors or of all their relationships.

## Population and the opening example

The [Foundation board roster](https://jupyter.org/governance/jupyter-foundation/) lists 13 people. The [SSC roster](https://jupyter.org/governance/software-subprojects/) lists 11 representatives, including the DEI representative. Their deduplicated union contains **24 people**. The [overview](https://jupyter.org/governance/overview/) and [directory](https://jupyter.org/governance/people/) agree on these displayed rosters. Names are matched to the GitHub logins explicitly supplied by Jupyter; logins are compared case-insensitively. No identities are inferred from names, emails or private membership.

There is a public-data inconsistency: the Foundation membership rule includes the whole Executive Council, but the displayed board table omits EC member Martha Cryan. She is already included through the SSC table, so resolving the table does not change this episode's union. We retain the displayed evidence and record the inconsistency rather than inventing a board entry or adding a separate EC population. [Retained roster](data/leadership-roster.json); [upstream CC0 roster data](data/sources/jupyter-contributors.yml), blob `aa8f16469ba1eb33a55c1c643df36d926aee826f`.

[Brian Granger appears on PyTorch's current Governing Board](https://pytorch.org/governing-board/). Jupyter's [current directory](https://jupyter.org/governance/people/) lists his Executive Council term, 2023–2024, and Foundation service under **former** leadership. An end year of 2026 in a former-role table is not evidence of a current appointment. He is a verified historical Jupyter/current PyTorch bridge and the article's entry point, **outside both measured populations**. We do not change the current-roster definition to include him.

## Week 1 continuity and fresh collection

We reviewed [Week 1 research](../week1/research.md), [its data guide](../week1/data/README.md), all three contributor tables and the existing SVG patterns before collection. Starting private main (`dc31788cd531e73503e7da6eabb50f7444a6960a`) contains no contributor-analysis functions, notebook or collector to import. We reuse its PR-opening measure, repository scoping, author aggregation, bot rule and blue/purple bar layouts. The new `collect.py` and `analyze.py` are small, episode-specific scripts. Week 1's bytes and its provenance gaps remain untouched. Before final review, the branch was updated to main `064e23a1327cfa039a8b72a74cc43214691cb341` and the revised canonical instructions, agenda and technical-material status were reread; that update does not change these research populations.

The PR-opening window is **[2026-01-01T00:00:00Z, 2026-10-08T00:00:00Z)**. Both open and closed PRs count, irrespective of eventual acceptance. Exact requests, collection timestamps, result totals and page sizes are in the collection manifests. The initial pages were collected through authenticated GitHub read access to public resources; remaining person pages used the unauthenticated public REST API at an eight-second minimum request interval after a temporary secondary rate limit. Every person query explicitly requests public records. No private repository, participant or account-administration evidence is used.

Queries, each sorted by creation ascending and paginated at 100 records:

```text
is:pr repo:jupyterlab/jupyterlab created:2026-01-01..2026-10-07
is:pr repo:jupyter-server/jupyter_server created:2026-01-01..2026-10-07
is:pr repo:ipython/ipykernel created:2026-01-01..2026-10-07
is:pr is:public author:<login> created:2026-01-01..2026-10-07
```

All 35 query populations fit below GitHub Search's 1,000-result ceiling. All successful responses reported `incomplete_results=false`. Each retained page set has a stable `total_count`, all expected page numbers, the corresponding number of projected raw records, unique PR URLs and in-window creation times. Initial incorrect pagination returned duplicates; those responses were rejected and discarded before analysis. The retained successful dataset has no duplicates. We retain PR number, URL, repository, creation time, author login/ID/type and `merged_at`, rather than copying PR bodies, contact details or unrelated profile data. This is a field projection of API records, not a full response archive.

### Exclusions and key-contributor selection

The Week 1 filter excludes GitHub user type `Bot` or a login ending in `[bot]`. We additionally exclude `meeseeksmachine`: its [public profile](https://github.com/meeseeksmachine) explicitly identifies a backport machine account even though the API type is `User`. This removes 112 additional JupyterLab PRs. The retained accounts are **not identified as bots**, not proven human authors or one-to-one identities. Missing authors would be excluded and reported; none occur in this sample.

| Component repository | All opened PRs | Excluded PRs | Retained PRs | Retained accounts | Fifth-place cutoff |
| --- | ---: | ---: | ---: | ---: | ---: |
| `jupyterlab/jupyterlab` | 882 | 215 | 667 | 157 | 21 |
| `jupyter-server/jupyter_server` | 91 | 13 | 78 | 38 | 4 |
| `ipython/ipykernel` | 77 | 21 | 56 | 23 | 5 |
| Combined | **1,050** | **249** | **801** | **195 distinct** | Per repository |

Select the **top five accounts in each repository, including every tie at the fifth-place PR count**, then deduplicate. This gives **12 key contributors in the Week 2 component sample**. Each repository contributes five accounts under these particular ties; the union is smaller because some recur. These accounts opened 446/801 retained PRs, **55.7%**, across the component sample. It is a purposive activity sample, not a random sample or a judgement about who matters most.

| Repository | Selected accounts and PR counts |
| --- | --- |
| JupyterLab | `krassowski` 152; `MUFFANUJ` 101; `jtpio` 47; `jasongrout` 26; `Darshan808` 21 |
| Jupyter Server | `krassowski` 14; `Carreau` 9; `Yann-P` 8; `aryansk` 4; `terminalchai` 4 |
| ipykernel | `Carreau` 13; `krassowski` 7; `JohanMabille` 5; `erikgaas` 5; `ianthomas23` 5 |

Four are also in the current leadership population: `krassowski`, `jtpio`, `johanmabille`, `Yann-P`. The two populations therefore have **32 unique accounts** in their union, not 36 independent observations. Contributor-only accounts without an explicit name mapping remain account logins.

## External relationships and classifications

Two evidence classes remain separate:

1. **Recent PR activity:** at least **three PRs opened by the recorded account in one repository** during the same 2026 window. This operational threshold identifies repeated submissions, not effort, influence or accepted work. Repositories qualify before any project grouping. PRs submitted in forks do not become contributions to their upstream parent by assumption. Every qualifying person/repository edge retains all direct PR URLs and its accepted-by-cutoff count.
2. **Documented role:** an explicit governance, core-team or maintainer listing. Roles do not require three PRs. A role's evidence date and period are retained, including dated recognition that does not establish a current appointment. A handful of inspectable role sources supplement the systematic PR pass; this is **not an exhaustive search of every external governance roster**.

All 32 accounts received the public-author query, including accounts with zero results. The 82 successful person pages contain **6,155 records**. Thirty results have the recorded opening account `Copilot`, rather than the searched person's login. They remain in raw data and [the exclusion table](data/excluded-search-records.csv), but are not reassigned to a person. Analysis uses **6,125 records**. We do not infer the mechanism, authorship or the person's responsibility for those 30 submissions.

The [project registry](data/project-registry.json) records a category, inclusion status, rationale, project grouping and direct evidence sources for every repository reaching the three-PR threshold:

- **Official Jupyter:** namespaces corresponding to the [public subproject list](https://jupyter.org/governance/list-of-subprojects/), plus Jupyter governance context. This includes IPython, Jupyter Book and JupyterHealth. The public list is a boundary proxy, not a private enterprise inventory or a census of active software.
- **Adjacent Jupyter:** external notebook extensions, kernels, deployment/integration work and associated tooling, such as Jupyter AI Contrib, GeoJupyter, Jupytext, 2i2c deployments and Nebari. These are distinguished from official subprojects and from independent non-Jupyter software.
- **Non-Jupyter:** independent software outside those boundaries, with an established open-source license. For example, conda-forge feedstocks count as contributions to packaging, **not** to the packaged upstream project's code. emscripten-forge and the xtensor stack are grouped by their respective project families; unrelated repositories owned by one company are not grouped into that company.

GitHub repository metadata was checked for all 213 non-official candidate repositories. Public metadata alone is not enough when GitHub reports no license or `NOASSERTION`; direct license checks resolve Pyflyby, NetworkX, NumPy, CPython, mypy, RQ, Sphinx and the conda-forge bot. Their sources are recorded in the registry. Polarctic's current Business Source License has a use restriction and is excluded from open-source counts. Remaining unresolved licenses stay **unclassified**, not proprietary by inference. Forks are conservatively excluded, including potentially maintained forks; websites, organizational planning, personal setup and test records are excluded as ancillary. These choices can undercount real external work. We do not search past the window, move a fork's work upstream, or classify an unlicensed public repository as open source.

## Results

| Evidence in the audited sources | Current leadership (24) | Component contributors (12) |
| --- | ---: | ---: |
| Qualifying recent non-Jupyter PR activity | **11 (45.8%)** | **10 (83.3%)** |
| Explicit non-Jupyter roles found in the supplementary role check | **3** | **1** |
| Either evidence class | **12 (50.0%)** | **10 (83.3%)** |
| Qualifying adjacent-Jupyter PR activity | 11 | 5 |

Rows overlap; do not add them. Role results are **documented matches in a limited audit**, not prevalence estimates comparable to the systematic PR pass. The contributor role is Ian Thomas's dated 2024 ContourPy core-maintainer recognition, not a newly verified appointment. Current leadership role matches are Chris Holdgraf (PyData Sphinx Theme), Min Ragan-Kelley (conda-forge and PyZMQ) and Sylvain Corlay (conda-forge). Corlay illustrates why a role and a recent-submission threshold are different measurements.

![At least three qualifying non-Jupyter PR submissions in one repository: 11 of 24 leaders, 45.8%; 10 of 12 component contributors, 83.3%. Groups overlap and missing evidence is unknown.](images/population-overlap.svg)

| Shared non-Jupyter project | Distinct qualifying accounts in the union | Leadership accounts | Component-contributor accounts | Inspectable account logins |
| --- | ---: | ---: | ---: | --- |
| conda-forge | 4 | 3 | 2 | `ianthomas23`, `johanmabille`, `martinrenou`, `minrk` |
| emscripten-forge | 3 | 2 | 2 | `ianthomas23`, `johanmabille`, `martinrenou` |
| PyData Sphinx Theme | 2 | 1 | 2 | `Carreau`, `Yann-P` |
| Pyflyby | 2 | 1 | 2 | `Carreau`, `krassowski` |
| QuantStack/git2cpp | 2 | 1 | 2 | `ianthomas23`, `johanmabille` |

The group columns overlap. In total, **94 non-Jupyter projects** meet the operational threshold, but only these five connect multiple sampled accounts; 89 connect one. The many single-account projects make a full network harder to read than these bars and table. The table is not a software dependency diagram. The project-grouping choices favor packaging families over individual feedstocks; rankings depend on those explicit choices.

![Most shared non-Jupyter projects by distinct sampled PR-opening accounts: conda-forge 4; emscripten-forge 3; PyData Sphinx Theme, Pyflyby and QuantStack/git2cpp 2 each. Role edges are separate.](images/shared-projects.svg)

For direct examples, use [all retained recent edges](data/recent-edges.csv) and [role evidence](data/role-evidence.json). Min Ragan-Kelley has ten 2026 PyZMQ PRs, all merged by the cutoff, **and** a separately documented package-maintainer role. Johan Mabille and Ian Thomas both reach the threshold in `QuantStack/git2cpp` and emscripten-forge recipes. Martha Cryan's recent activity includes seven marimo and four Plotly.js PRs; those submissions do not by themselves appoint her to either project's governance.

### Interpretation

The observed connections are broad and uneven. Shared packaging and documentation projects sit alongside many projects connected to one sampled account. Governance authority and submitted activity reveal different relationships. It is reasonable to investigate whether these people carry practical knowledge between communities, but these data do not measure conversations, collaborations between the named people, transfers of knowledge or consequent decisions. A shared project edge is not proof that its two contributors worked together.

### Limits that travel with every quantitative claim

- Public GitHub PR-opening activity omits reviews, direct commits, issue support, documentation outside PRs, organizing, mentoring and private/non-GitHub work.
- The 12 accounts are selected for high activity in three components. They do not represent all Jupyter contributors. The 24-person leadership roster is itself a chosen governance definition, excluding other forms of leadership and former members.
- Three submissions are an operational cutoff. Raising it, selecting another window or grouping projects differently would change the edges. It is not a scientific definition of substantial impact.
- A public roster and a contribution count measure different things. Accounts not labeled bots can still use automation or AI. No opinion, motive or policy position is inferred.
- Unknown licenses, fork exclusion, missing identities and the limited role audit leave real relationships unobserved. An empty field is not evidence of no connection.
- Collection is not an atomic GitHub snapshot. Old PRs can be deleted, transferred or have metadata change; matching counts and unique URLs verify the retained extraction, not that GitHub will return identical results indefinitely. `merged_at` is observed during collection and compared to the fixed cutoff.

## Reproduction, visual review and next check

Run `python week2/data/analyze.py` from a checkout to reproduce every generated table, `summary.json` and both SVGs **offline with Python's standard library**. The [data guide](data/README.md) describes a separate fresh-collection command, schemas, inclusion rules and validation. `collect.py` stops on API errors and on incomplete/oversized searches; a rerun creates a separately dated directory and cannot repair Week 1's historical gaps.

The SVGs adapt Week 1's white background, blue/purple bars, typography, explicit denominators and caveat footers. Both were rendered and visually inspected at their native 1,100-pixel screen-sharing width: labels, bars, values, margins and caveat footers are legible without clipping. No new logo is made. The article uses the existing approved `assets/the-eye-logo.webp`. Offline regeneration reproduces the output bytes; population counts, project rankings, direct-example counts and relative links were checked against the retained inputs and final repository tree. The article is within the 600–900 word target. No teaching model or external inference API is needed for this analysis.

Next useful check: resolve the Foundation board table's EC omission upstream and extend the role audit **within this same population** if a later episode needs stronger governance comparisons. Do not broaden to a Jupyter-wide contributor census or a global social network without a new scope decision. Nothing in this branch is approved for publication.

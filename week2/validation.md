# Week 2 notebook validation

**Issue:** #15. **Final status:** Goals 0–3 and testing were accepted October 7, 2026 (America/Los_Angeles). Private PR #16 was merged and #15 was closed. Publication is reviewed separately from technical acceptance.

## Goal 0 — workspace checks, October 3, 2026

### Tested environment

Fresh native conda environment on Linux x86_64, built from `environment.yml`. Miniconda 26.7.1's terms plugin checked unrelated defaults despite `nodefaults`; creation succeeded with `conda --no-plugins env create --solver classic -f week2/environment.yml`. No default-channel terms were accepted. The conda transaction used conda-forge; application packages came from pip.

| Component | Tested version |
| --- | --- |
| Python | 3.12.14 |
| PyTorch | 2.8.0+cpu |
| JupyterLab | 4.4.9 |
| Jupyter Server (transitive) | 2.21.1 |
| ipykernel | 6.30.1 |
| Transformers | 4.56.2 |

Model: [M-FAC/bert-tiny-finetuned-sst2](https://huggingface.co/M-FAC/bert-tiny-finetuned-sst2/tree/41ad6709ec46b414749b37daf49cf5ca1c7dba7c), revision `41ad6709ec46b414749b37daf49cf5ca1c7dba7c`. Downloaded weights: 17,564,583 bytes. Model source is separate from the PyTorch library. The source card lacks explicit license metadata; no weights or dataset are committed or redistributed here.

### Passed

- Fresh environment creation and imports; `pip check` found no broken requirements.
- Notebook schema validation, warning before code, and empty saved outputs/execution counts.
- The exact notebook code cells executed top-to-bottom in the environment's Python process, with a fresh model cache. CPU output had shape `(1, 2)`, finite scores summing to one.
- `This movie was wonderful.` produced positive, with scores negative `0.0035`, positive `0.9965`.
- A second fresh Python process loaded from the cache with `HF_HUB_OFFLINE=1`, repeated the cells and ran a changed input. `This movie was terrible.` produced negative, with scores negative `0.9912`, positive `0.0088`.
- JupyterLab started using the environment's Python. Its `/lab` page and notebook Contents API each returned HTTP 200. The server was stopped after testing.

These example predictions verify execution, not accuracy, fairness or calibration.

### Historical workspace limitation

The normal nbclient/ipykernel run failed before executing any cell: this managed sandbox denied network-interface/socket operations (`Operation not permitted`, kernel died before `kernel_info`). An IPC attempt also failed at socket binding. Neither attempt establishes a notebook/model error, and neither counts as a successful kernel run. No sandbox-specific workaround was added to the teaching environment or notebook.

## Goal 0 — Mac acceptance, October 7, 2026

Rick tested the branch notebook through JupyterLab in the native `jupyter-pytorch-week2` conda environment. The warning path confirms Python 3.12; exact macOS and package patch versions were not collected in this acceptance exchange.

- Positive sentence: positive, scores negative `0.0035`, positive `0.9965`.
- Changed negative sentence: negative, scores negative `0.9912`, positive `0.0088`.
- Restart Kernel and Run All Cells: passed, with the same negative result.
- Server shutdown, relaunch with `HF_HUB_OFFLINE=1`, and a fresh-kernel run: passed with the same negative result.
- Optional `IProgress`/tqdm widget warning did not block execution.

Rick declared Goal 0 complete and explicitly authorized Goal 1. This is user-reported laptop acceptance, separate from the earlier workspace checks. No claim of Apple GPU operation was made.

## Goal 1 — instrumentation

The companion `instrumented-pytorch.ipynb` uses the same environment/model. It shows at most 16 token positions, input tensor shapes/dtypes/devices, embedding and encoder stage outputs, pooling/classification outputs, four sample values per stage, logits and softmax scores. Hooks are temporary and do not replace outputs. Process/environment observations and repository walkthroughs remain Goals 2–3.

### Workspace checks — October 8, 2026 UTC (October 7 in San Diego)

Executed the companion's exact code cells in a fresh Python process on Linux x86_64, using Python 3.12.14, PyTorch 2.8.0+cpu, Transformers 4.56.2 and ipykernel 6.30.1. These runtime checks used a scratch venv with the existing pins; the earlier clean conda solve was not repeated because the checked-in environment is unchanged.

- Notebook schema, safety warning, empty saved outputs/counts and `pip check`: passed.
- Positive and negative examples reproduced Goal 0's rounded scores.
- Observed shapes for the seven-token examples: embeddings and both encoder layers `(1, 7, 128)`; pooler `(1, 128)`; classifier `(1, 2)`. All reported CPU.
- Instrumented logits matched the same model's uninstrumented forward pass exactly.
- Repeated observation runs produced five stage rows without accumulating hooks. Invalid input caused an inference error and still removed all hooks; a subsequent valid run worked.
- A 200-word input was truncated to 128 tokens. Tables stayed limited to 16 token rows and four values per stage. Input text is displayed up to 200 characters. HTML table values are escaped.
- A fresh process with `HF_HUB_OFFLINE=1` executed all cells using cached model files.

The [pinned Transformers BERT implementation](https://github.com/huggingface/transformers/blob/v4.56.2/src/transformers/models/bert/modeling_bert.py) was checked for pooling/classifier semantics; [PyTorch 2.8 hook documentation](https://docs.pytorch.org/docs/2.8/generated/torch.nn.Module.html#torch.nn.Module.register_forward_hook) was checked for observation and removal behavior. Stage samples illustrate numerical flow, not feature meanings or hardware profiling.

### Mac acceptance — October 7, 2026

Rick reported successful runs with varying sentences, confirmed Restart Kernel and Run All Cells, and said the tables looked good. He declared Goal 1 complete and authorized Goal 2. This is user-reported JupyterLab acceptance; no additional exact OS/package versions were collected.

## Goal 2 — components and kernel state

The instrumented notebook now identifies the Python executable/environment, PID/parent PID, actual shell/kernel classes, PyTorch import/version, installed package metadata, and model source/revision/class/device. UI/server observations are explicit manual checks; installed packages are not represented as proof of the running server or frontend. It does not inspect credentials, connection files, broad environment variables, or make server-discovery requests.

The state probe increments in a live namespace and runs alone after a restart: fresh state starts at 1 without a loaded model. The document, interface, server, kernel, environment, tensor library and checkpoint have separate runtime roles. The notebook keeps the repository/process walkthrough for Goal 3.

### Workspace checks — October 8 UTC (October 7 in San Diego)

- Notebook schema, empty saved outputs and exact code-cell execution offline in ordinary Python: passed, including the explicit no-kernel fallback.
- Exact cells executed in an actual in-process ipykernel: passed; diagnostics correctly identified that kernel/shell context. This does not verify a separate JupyterLab/server/kernel deployment.
- Existing positive CPU prediction and five stage observations remained valid.
- State probe increments from 1 to 2 in a shared namespace; in a fresh namespace it starts at 1 with no model. The probe is independently runnable because it imports its own required module.
- No dependencies or model pins changed. Earlier clean conda creation was not repeated. Runtime pins remain those recorded under Goal 1.

Architecture/role claims were checked against [Jupyter Server architecture](https://jupyter-server.readthedocs.io/en/stable/developers/architecture.html), [JupyterLab documents/kernels](https://jupyterlab.readthedocs.io/en/4.4.x/user/documents_kernels.html), [Running panel behavior](https://jupyterlab.readthedocs.io/en/4.4.x/user/running.html) and the [notebook format](https://nbformat.readthedocs.io/en/latest/format_description.html).

### Mac acceptance — October 7, 2026

Rick reported that the notebook is functional through restarts and explicitly declared Goal 2 complete. This records user-reported acceptance, not a new collection of individual UI/server observations or runtime versions.

Windows and Apple MPS/GPU remain untested. Only direct package versions and the model revision are pinned; transitive dependency versions may change in future solves. These remain limitations of the accepted demonstration; publication is reviewed separately from technical acceptance.


## Goal 3 — source and development walkthrough

Implementation was prepared October 8 UTC (October 7 in San Diego) and subsequently accepted as Goal 3. The two notebooks add Markdown source entry points; their previously accepted executable cells are unchanged. The component guide maps upstream projects and uses the observed restart behavior to follow documentation, source, contribution guidance and execution-test evidence. No upstream issue/PR is presented as a fix for expected restart behavior, and no report was submitted.

### Workspace checks

- Both notebook schemas and empty outputs/counts: passed. Exact code-cell JSON values match the accepted Goal 2 revision; `environment.yml` is byte-for-byte unchanged.
- Both notebooks' exact cells ran in fresh ordinary-Python namespaces with the existing cache and `HF_HUB_OFFLINE=1`; both produced the baseline positive prediction. This check is separate from accepted Mac JupyterLab restart behavior. No new conda solve or upstream test suite was run.
- Seventeen unique release-tagged GitHub source links resolved; their line anchors are within the downloaded files. The selected JupyterLab cell/output-area/kernel-request path, Server message relay and ipykernel execution branch were read, rather than inferred from package names.
- Installed ipykernel `Kernel.execute_request` / `IPythonKernel.do_execute`, IPython `InteractiveShell.run_cell` / `run_cell_async`, PyTorch `Module._call_impl` / `register_forward_hook`, and Transformers `BertForSequenceClassification.forward` matched the tagged source's signatures and executable bodies (ignoring decorators/docstring indentation). Current scratch IPython is 9.17.1, a transitive dependency. Earlier clean-conda validation recorded JupyterLab 4.4.9 and Server 2.21.1; neither is installed in the current scratch venv. Mac patch versions remain uncollected.
- Mermaid source parsed and rendered with Mermaid CLI 11.12.0. The diagram retains the browser outside the environment, separate server/kernel boxes and request/result directions. Rendering tools are scratch-only, not teaching-environment dependencies.
- At Rick's request, the SVG was removed and the same Mermaid diagram is embedded directly in the instrumented notebook and component guide. Both embed the exact checked-in `.mmd` source. Ordinary repository links sit beside the diagram. No SVG file or SVG references remain in the demonstration materials. This workspace check did not separately record native-laptop rendering/navigation evidence; Rick later accepted Goal 3 and testing as complete.


The core map/model-source/restart-question route fits the existing first-half deployment walkthrough. The detailed source table is optional reference; no agenda, Eye article, Git tutorial, environment pins, model revision or runtime behavior was changed. Rick subsequently accepted Goal 3 and testing as complete; private PR #16 was merged. Publication remains a separate exact-file review.


### Requested notebook split — October 7, 2026

Rick requested removal of the Markdown section “From an observation to an open-source question” and a separate mapping notebook. That section and its referring links were removed. `component-mapping.ipynb` now contains component roles, runtime identity, UI/server comparisons, the state experiment, Mermaid diagram and source/project links. It runs independently without loading model weights; its observations refer to its own kernel. The state probe explains why model presence is normally false in this notebook.

The instrumented notebook retains the model identity/device table, encoding, stage hooks and scores. Its small `class_name` helper moved alongside the display helper so that removing runtime diagnostics introduces no hidden dependency. Model loading, encoding, forward computation, hook cleanup and prediction cells are unchanged. The minimal notebook's executable cells and the environment are unchanged. Its existing guide reference was adjusted to omit the removed question section.

Both the instrumented and mapping notebooks passed schema/empty-output checks and independent exact code-cell execution offline in fresh ordinary-Python namespaces. The instrumented notebook reproduced the positive baseline; the mapping notebook ran without loading a model and started its probe at 1. No separate Mac evidence for the reorganized notebooks was recorded in this step; Rick later accepted Goal 3 and testing as complete.


### Consolidate the mapping guide — October 7, 2026

At Rick's request, the Markdown component guide was deleted after consolidating its unique content into `component-mapping.ipynb`. The notebook now contains the full ten-project table (including CPython, conda, checkpoint and nbformat), the complete nine-row tagged execution-path table, source-version caveats, cache/process-boundary explanations and brief optional-reference guidance. The existing diagram and observations remain. All external URLs from the deleted guide are retained in the notebook; duplicate shorter project/source passages were replaced rather than appended. Setup and minimal-notebook links now point to the mapping notebook.

Notebook schema and empty-output checks passed. Mapping and minimal executable cells are unchanged; no model/environment change or repeat inference test was needed for this Markdown-only consolidation. No additional laptop evidence was recorded for this Markdown-only step before final Goal 3 acceptance.


## Final acceptance

Rick accepted Goals 0–3 and the recorded testing as complete on October 7, 2026 (America/Los_Angeles). Private PR #16 was merged and issue #15 was closed. That acceptance did not add evidence beyond the checks and user-reported observations recorded above; in particular, exact Mac patch versions, Windows execution, Apple MPS/GPU execution and a separate native-laptop rendering check were not collected.

This validation record documents the accepted technical state. Publication is a separate decision based on review of the exact participant-facing files.

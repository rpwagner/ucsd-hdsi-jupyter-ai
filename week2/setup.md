> **Trust but verify.** Even examples Rick shares and AI-generated suggestions can be wrong or unsafe. Read code, commands and configuration before running them; use disposable copies, keep backups, and verify results. Don't let an example eat your homework.

# Run the Week 2 notebooks

You can participate by watching Rick's demonstration: no installation or account is required. This is an optional native conda setup, not a synchronized installation exercise. Use a disposable checkout/copy of these files rather than a coursework folder.

With conda already installed, run these commands from the repository root:

```bash
conda env create -f week2/environment.yml
conda activate jupyter-pytorch-week2
python -m jupyterlab --notebook-dir=week2
```

Open `minimal-pytorch.ipynb`, choose **Python 3 (ipykernel)**, and use **Kernel → Restart Kernel and Run All Cells**. The output should show `Model ready on cpu`, the input sentence, a prediction, and two scores. Change the sentence and rerun the prediction cell.

After the baseline, open `instrumented-pytorch.ipynb` to inspect encoding, input tensors, selected model stages and scores. It uses the same environment and cache; no reinstall is needed. When changing the sentence, rerun the encoding cell and every cell below it.

Then open `component-mapping.ipynb` for the separate process, code and open-source project walkthrough. Run all cells to identify its kernel/Python environment; compare the package table with the interface and server terminal, then use its state probe to inspect what a restart clears. It does not load a model. Notebooks can have separate kernels, so these process observations describe the mapping notebook's own kernel. The mapping notebook also contains the full project and source-path tables.

A `TqdmWarning: IProgress not found` warning concerns the optional download-progress widget. It does not block inference; widgets are not required here.

The environment uses conda-forge for Python and pip, then pip for four direct application dependencies: PyTorch, JupyterLab, ipykernel (the Python kernel), and Transformers (the selected model's tokenizer and BERT definition). Dependencies of these packages are installed automatically. Linux/Windows use the CPU-only PyTorch wheel; macOS uses its standard wheel, with the notebook explicitly keeping computation on CPU. No torchvision, torchaudio, datasets, training or profiling packages are requested. These are tested pins, not a claim to use the latest releases.

If Miniconda reports an unrelated default-channel terms check even though the file excludes defaults, use the plugin-free classic solver for creation:

```bash
conda --no-plugins env create --solver classic -f week2/environment.yml
```

## Download and offline use

The first load needs network access to Hugging Face for a public tokenizer, configuration and roughly 17 MB of pretrained weights. No token or account is required. Loading uses a fixed revision, disables remote model code and uses PyTorch's restricted weights loader. It does not make a network inference call; your input is processed locally.

The [model card](https://huggingface.co/M-FAC/bert-tiny-finetuned-sst2/tree/41ad6709ec46b414749b37daf49cf5ca1c7dba7c) identifies BERT-tiny fine-tuned on SST-2. The [SST-2 dataset card](https://huggingface.co/datasets/stanfordnlp/sst2) documents the class order used here: negative (0), positive (1). The checkpoint configuration does not name those labels, so the notebook supplies that mapping explicitly. The model can misclassify text, and scores are not calibrated confidence estimates. Inputs are truncated at 128 tokens.

After one successful run, stop JupyterLab and relaunch it with downloads disabled to verify that the cache is complete:

```bash
HF_HUB_OFFLINE=1 python -m jupyterlab --notebook-dir=week2
```

This command sets offline mode only for that server launch. To allow downloads again, stop it and launch normally. Stop the server with Ctrl-C and confirm shutdown when prompted. Restarting the kernel clears live variables/model state; it does not remove downloaded files or saved notebook outputs. Clear outputs before committing or sharing a changed notebook.

## Validation status

Goals 0–3 and testing were accepted on October 7, 2026, and the completed Week 2 notebook work was merged through private PR #16. The minimal notebook remains the baseline; the instrumented notebook exposes model internals; and `component-mapping.ipynb` contains the process, repository and source-path walkthrough. Open the mapping notebook after the model demonstration; no new environment setup is needed.

See [validation.md](validation.md) for the checks, evidence and remaining limits. Publication is reviewed separately from technical acceptance, using the exact candidate files.

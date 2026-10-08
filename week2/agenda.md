# Week 2 Agenda

> [!WARNING]
> **Trust but verify.** Even examples Rick shares and AI-generated suggestions can be wrong or unsafe. Read code, commands and configuration before running them; use disposable copies, keep backups, and check what files and tools an agent can access. Don't let an example eat your homework.

**Jupyter on your laptop**<br>
**Thursday, October 8, 2026 | 3:00-4:30 PM**<br>
**HDSI, Room 210 | UC San Diego local time**

## 3:00 - First half: What happens when you press Run?

### Intro and Recap

Get settled, reconnect and carry forward questions from Week 1. Start with a question we can investigate: when a model produces an answer in a notebook, what actually did the work?

### Follow a sentence from notebook to prediction

We will open a disposable notebook, load a small BERT text-classification model through [Transformers](https://github.com/huggingface/transformers) backed by [PyTorch](https://pytorch.org/), and give it a short phrase. We will use that running deployment to investigate Jupyter's components and the model's behavior, then connect our observations to the code and open-source process behind them.

**Find the pieces on the laptop.** Separate the notebook document from the interface in the browser, the [Jupyter Server](https://jupyter-server.readthedocs.io/en/stable/developers/architecture.html), and the Python kernel executing our cells. Identify the Python environment and running process, and distinguish the notebook's saved content from the variables and model held in the kernel's memory. The notebook is our window into the computation, not the whole computer.

**Follow the information as it changes.** Trace the input text through tokenization and numerical encoding into tensors, then through model layers and intermediate values to output scores and a readable classification. Inspect selected values and shapes along the way. We will run a [forward pass](https://docs.pytorch.org/docs/stable/notes/modules.html) with trained weights, not train a model during the session.

**Locate the work on the hardware.** Inspect device placement and confirm where the tested demonstration is executing on the CPU. The goal is to make the stages and their location visible, not to require a powerful laptop or make an untested GPU-performance claim.

### From running components to code and changes

Map the pieces we just used to their source repositories:

| Piece in the demonstration | What we will connect it to | Source repository |
| --- | --- | --- |
| JupyterLab | The notebook interface in the browser | [jupyterlab/jupyterlab](https://github.com/jupyterlab/jupyterlab) |
| Jupyter Server | Notebook files, kernel management and communication | [jupyter-server/jupyter_server](https://github.com/jupyter-server/jupyter_server) |
| ipykernel / IPython | The Python kernel process, cell execution and live state | [ipython/ipykernel](https://github.com/ipython/ipykernel) · [ipython/ipython](https://github.com/ipython/ipython) |
| PyTorch | Tensor operations used by the model | [pytorch/pytorch](https://github.com/pytorch/pytorch) |
| Transformers | The BERT model and tokenizer implementation built on PyTorch | [huggingface/transformers](https://github.com/huggingface/transformers) |
| Model / weights | The pinned BERT-tiny SST-2 checkpoint loaded into the kernel | [M-FAC/bert-tiny-finetuned-sst2](https://huggingface.co/M-FAC/bert-tiny-finetuned-sst2/tree/41ad6709ec46b414749b37daf49cf5ca1c7dba7c) |

The component-mapping notebook also links selected visible actions—such as running a cell and executing the model—to release-tagged implementation functions in JupyterLab, Jupyter Server, ipykernel/IPython, PyTorch and Transformers.

Use one observed behavior or question to navigate a repository's README, contribution guidance, issues and pull requests. Find where a problem is reported, how a proposed change is reviewed, and what evidence or tests help establish that it works. This connects a component on our laptop to an open-source development process we can inspect and participate in, without requiring anyone to submit code.

### The Eye: The people between the projects

A brief, data-focused look at overlap between Jupyter leadership, key contributors and other open-source projects, beginning with the Jupyter/PyTorch connection. Read [The Eye](the-eye.md), [research](research.md) and [supporting data](data/README.md).

## Around 3:45 - Second half: Your questions and projects

Stay for optional small-group and individual discussion and help. What are you trying to do? Bring a question, start something, or get help making progress on work you have already begun. You are welcome to revisit today's example, but this is not a continuation of the prepared demonstration. No project or installation is required.

## Session resources

**Demonstration materials:** [minimal PyTorch notebook](minimal-pytorch.ipynb) · [instrumented PyTorch notebook](instrumented-pytorch.ipynb) · [component/process/source mapping notebook](component-mapping.ipynb) · [setup](setup.md) · [environment.yml](environment.yml) · [validation record](validation.md). The prepared example uses a native conda environment and CPU execution, without a container or external model API. No installation is required to participate by watching.

**Optional references:** [Project Jupyter](https://jupyter.org/) · [JupyterLab documents and kernels](https://jupyterlab.readthedocs.io/en/stable/user/documents_kernels.html) · [PyTorch tutorials](https://docs.pytorch.org/tutorials/).


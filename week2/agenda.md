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

We will open a disposable notebook, load a small downloaded text-classification model with [PyTorch](https://pytorch.org/), and give it a short phrase. We will use that running deployment to investigate Jupyter's components and the model's behavior, then connect our observations to the code and open-source process behind them.

**Find the pieces on the laptop.** Separate the notebook document from the interface in the browser, the [Jupyter Server](https://jupyter-server.readthedocs.io/en/stable/developers/architecture.html), and the Python kernel executing our cells. Identify the Python environment and running process, and distinguish the notebook's saved content from the variables and model held in the kernel's memory. The notebook is our window into the computation, not the whole computer.

**Follow the information as it changes.** Trace the input text through tokenization and numerical encoding into tensors, then through model layers and intermediate values to output scores and a readable classification. Inspect selected values and shapes along the way. We will run a [forward pass](https://docs.pytorch.org/docs/stable/notes/modules.html) with trained weights, not train a model during the session.

**Locate the work on the hardware.** Inspect device placement and connect the operations to the CPU, with an [Apple GPU comparison](https://docs.pytorch.org/docs/stable/notes/mps.html) where supported. Which parts stay in Python on the CPU, and which tensor operations can run on a GPU? The goal is to make the stages and their location visible, not to require a powerful laptop or assume that a GPU is always faster.

### From running components to code and changes

Map the pieces we just used to their source repositories:

| Piece in the demonstration | What we will connect it to | Source repository |
| --- | --- | --- |
| JupyterLab | The notebook interface in the browser | [jupyterlab/jupyterlab](https://github.com/jupyterlab/jupyterlab) |
| Jupyter Server | Notebook files, kernel management and communication | [jupyter-server/jupyter_server](https://github.com/jupyter-server/jupyter_server) |
| IPython kernel | The Python process executing cells and keeping live state | [ipython/ipykernel](https://github.com/ipython/ipykernel) |
| PyTorch | The tensor operations and model layers used by our Python code | [pytorch/pytorch](https://github.com/pytorch/pytorch) |

We will also identify where the selected model and its downloaded weights come from; those are distinct from the PyTorch library itself. That source will be added when the example is selected.

Use one observed behavior or question to navigate a repository's README, contribution guidance, issues and pull requests. Find where a problem is reported, how a proposed change is reviewed, and what evidence or tests help establish that it works. This connects a component on our laptop to an open-source development process we can inspect and participate in, without requiring anyone to submit code.

### The Eye: Why Open Source Still Meets in Person

A brief introduction to the week's story. The article will be prepared separately and shared for reading after the session.

## Around 3:45 - Second half: Your questions and projects

Stay for optional small-group and individual discussion and help. What are you trying to do? Bring a question, start something, or get help making progress on work you have already begun. You are welcome to revisit today's example, but this is not a continuation of the prepared demonstration. No project or installation is required.

## Session resources

**Demonstration materials:** the notebook and package/install instructions are still being prepared. The example will use a native Python/Jupyter environment, without a container; conda is optional. No external model API is required.

**Optional references:** [Project Jupyter](https://jupyter.org/) · [JupyterLab documents and kernels](https://jupyterlab.readthedocs.io/en/stable/user/documents_kernels.html) · [PyTorch tutorials](https://docs.pytorch.org/tutorials/).

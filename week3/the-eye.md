<p align="center"><img src="../assets/the-eye-logo.webp" alt="The Eye: the approved red planetary-eye artwork" width="300"></p>

# The Eye - Week 3

## From chat to tools: how AI took shape around Jupyter

**Evidence through October 14, 2026 UTC | Sources checked October 15, 2026**

Getting AI software to answer a question inside a notebook is one achievement. Getting it to change a cell, run it, and show the result reliably is another. The public history of AI software around Jupyter shows developers tackling both, then making pieces reusable across assistants. The work includes experiments, shared interfaces and the less visible effort of making extensions coexist.

![Timeline: December 2022 Jupytee experiment; August 2023 Jupyter AI launch; June 2024 Codestral experiment, later JupyterLite AI; October 2025 Jupyter AI code split announced; April 2026 Jupyter AI 3.0 with ACP agents and MCP tools; September 2026 Jupyter AI 3.2 with shared commands and optional JSD.](images/ai-timeline.svg)

*Selected milestones; completion, chat and agents coexist. Dates use UTC. [Event sources](data/timeline.csv).*

### Several beginnings

In December 2022, [Jupytee](https://github.com/fperez/jupytee/commit/47b8c75bc7b654b8c084471489381bd60dd1cf7a) described itself as an experimental playground connecting GPT-3 models—software that generates responses to prompts—to Jupyter through *magics*: special commands typed into notebook cells. Other developers explored chat and code suggestions. These were different entry points, not one project unfolding under different names.

AI assistance already had a foothold. A [January 2023 JupyterLab proposal](https://github.com/jupyterlab/jupyterlab/pull/13804) named Kite and Tabnine as earlier code-completion integrations—suggestions that finish code as someone types—then proposed broader tasks such as explaining selected code. Chat experiments were not the beginning of all AI in Jupyter.

That August, [Jupyter AI's launch](https://blog.jupyter.org/posts/2023/generative-ai-in-jupyter/) brought chat and magics together with a choice of models. Users could ask about code, request changes or generate notebooks. The announcement credited five builders. There is no established code lineage here from Jupytee into Jupyter AI; similar goals do not prove shared code.

### A personal experiment becomes shared machinery

Another path began with code completion. In June 2024, the project now called JupyterLite AI had an [experimental README](https://github.com/jupyterlite/ai/blob/9c8d350b8876ad3a9ffe8dbe723ca093bb680681/README.md) naming the personal repository `jtpio/jupyterlab-codestral`. It connected Mistral's models to completions and chat, including use in JupyterLite, where notebook code can run inside the browser. A [December rename](https://github.com/jupyterlite/ai/pull/20) broadened the project's name.

Integration continued well beyond renaming. In July 2026, contributor `brichet`'s [accepted code change](https://github.com/jupyterlite/ai/pull/356) introduced a browser-side *persona*: an assistant connected to a chat. The aim was to use shared chat infrastructure rather than require a separate chat system. The proposal also recorded a compatibility blocker: messages could not yet propagate through Jupyter Chat as needed.

By September, [Jupyter AI 3.2's release notes](https://github.com/jupyterlab/jupyter-ai/blob/5b23f55d15ba245347013ffe0a238f26b1f4f1e8/docs/source/releases/v3.2.0.md) documented a concrete connection: its notebook tools used the same frontend commands as JupyterLite AI. These commands perform actions such as editing and running cells through the browser interface. Shared operations could serve different assistants without making those assistants identical.

The people crossed repository boundaries too. In **10 of 12 deliberately selected histories**, at least one early contributor had an earlier contribution accepted in Jupyter or IPython, the interactive Python project from which Jupyter grew. Seven cases began in personal repositories. This is a sample of project histories, not a census of the ecosystem. [Evidence and selection](research.md#quantitative-results-and-their-limits).

![Initial repository settings across 12 selected cases: official Jupyter 1 documented prior contributor, 0 unknown; personal 5 documented, 2 unknown; company 1 documented, 0 unknown; contrib 2 documented, 0 unknown; unresolved setting 1 documented, 0 unknown.](images/origin-inventory.svg)

*The graphic separates where code first appeared publicly from prior contributor evidence. Personal and company labels do not identify funding, employer support or community membership; unknown history does not mean newcomer. [Methods](data/selection.md).*

### Connecting assistants—and keeping notebooks consistent

An *agent* uses a model and tools to take actions across several steps. In its [February 2026 release plan](https://github.com/jupyterlab/jupyter-ai/issues/1531), Jupyter AI's maintainers reported reliability and maintenance difficulties with their own agent, Jupyternaut. They prioritized connecting external agents instead. That was their account of the tradeoff, not an independent performance benchmark.

Two protocols—agreed ways for programs to communicate—support that division of work. **Agent Client Protocol (ACP)** connects an agent to Jupyter AI's interface, including progress and permission requests. **Model Context Protocol (MCP)** exposes tools an agent can call, such as notebook operations. The [v3.0 release](https://github.com/jupyterlab/jupyter-ai/releases/tag/v3.0.0) documented both integrations.

Those connections still need reliable document handling. **Jupyter Server Documents (JSD)** handles documents on the server and helps track kernels, the processes that execute notebook code. In a [June compatibility discussion](https://github.com/jupyter-ai-contrib/jupyter-server-documents/issues/239), David Qiu explained its role in making agent edits appear consistently, but reported conflicts with other extensions and proposed changes. One affected Voilà, which turns notebooks into dashboards. The discussion credited earlier community work and proposed reducing JSD's changes to existing Jupyter behavior.

The [September 3 release](https://github.com/jupyterlab/jupyter-ai/blob/5b23f55d15ba245347013ffe0a238f26b1f4f1e8/docs/source/releases/v3.2.0.md) made JSD and real-time collaboration—keeping multiple users' views synchronized—optional while retaining notebook editing and execution through frontend commands. That is a documented change, not proof that the June issue alone caused it. JSD remained available as an optional integration.

The release also fixed tool commands running in every browser connected to a server, restricting them to the browser that triggered the request. Integration includes deciding which session an action affects.

Packaging was consequential work too. The [October 2025 split announcement](https://github.com/jupyterlab/jupyter-ai/issues/1495) described reorganizing existing Jupyter AI code into ten focused packages under `jupyter-ai-contrib`, a separate GitHub organization hosting code repositories. Chat commands, personas and notebook tools gained distinct package boundaries. The intended benefit was reusable building blocks with separate versions. Counting those packages as independent inventions would misread their history.

Completion, chat, commands and agents can coexist. The consequential change in these episodes is that notebook capabilities became reusable across implementations—and required continued integration and maintenance. As assistants share more interfaces, **what should Jupyter itself be responsible for, and what belongs to the surrounding tools?**

---

[Research and primary-source record](research.md) | [Inventory selection and limitations](data/selection.md)

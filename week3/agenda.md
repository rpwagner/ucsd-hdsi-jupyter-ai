# Week 3 Agenda

> [!WARNING]
> **Trust but verify.** Even examples Rick shares and AI-generated suggestions can be wrong or unsafe. Read code, commands and configuration before running them; use disposable copies, keep backups, and check what files and tools an agent can access. Don't let an example eat your homework.

**Jupyter AI on your laptop**<br>
**Thursday, October 15, 2026 | 3:00-4:30 PM**<br>
**HDSI, Room 210 | UC San Diego local time**

*The direct Ollama model-chat path has instructor acceptance. The prepared container now includes notebook tools over MCP/JSD and Goose over ACP, with automated container and browser checks against a synthetic model. The complete live Mac/Ollama rehearsal is still pending. We will show only verified live behavior, with static explanations for anything not ready.*

## 3:00 - First half: Give a notebook an AI collaborator

### Intro and Recap

Recall the notebook, Jupyter Server and Python kernel from Week 2. This week we add an AI assistant and ask: when it explains code, edits a cell or executes code, which piece is actually doing the work?

### First, talk to a model

Open a disposable notebook in a prepared [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) teaching container. Add a simple [Jupyter AI](https://jupyter-ai.readthedocs.io/en/stable/users/) persona (the chat connection to a model) and inspect a small code-explanation request. The selected instructor model runs in [Ollama](https://ollama.com/) on the laptop, outside the teaching container, and is reached through an OpenAI-compatible API.

Compare the notebook's saved cells and kernel state with the chat request and its **redacted** response. Chat can explain a pasted snippet without itself editing the notebook or running a cell. The [starter notebook](minimal-chat.ipynb), [companion](companion.md) and [stage-one diagram](images/stage1-model-api.svg) show the pieces and an offline fallback.

### Then, give the assistant notebook tools

The next persona connects a [Jupyter MCP server](https://github.com/jupyter-ai-contrib/jupyter-server-mcp) and three reviewed notebook tools backed by [Jupyter Server Documents (JSD)](https://github.com/jupyter-ai-contrib/jupyter-server-documents). MCP lets software request a tool action; it does not make a model's text response an executed command.

On a disposable notebook, inspect a proposed small cell change or safe execution, review the action and verify the saved document and live kernel result independently. JSD is an optional integration in this example, not a requirement for every Jupyter AI installation. We will not present a simulated tool exchange as a completed live test.

### Finally, connect an external agent

The final persona connects [Goose](https://block.github.io/goose/) through the [Agent Client Protocol (ACP) integration](https://github.com/jupyter-ai-contrib/jupyter-ai-acp-client). Repeat a comparable notebook task and distinguish the model API, the chat-to-agent connection (ACP) and the agent's access to tools (MCP). Inspect what each process can read, change or execute, and where permission checks apply.

### Follow the software into its repositories

| What we inspect | Project code |
| --- | --- |
| Chat, personas and agent hosting | [Jupyter AI](https://github.com/jupyterlab/jupyter-ai) |
| Model-chat teaching integration | [Week 3 starter notebook](minimal-chat.ipynb) and [companion](companion.md) |
| Notebook tools over MCP | [Jupyter Server MCP](https://github.com/jupyter-ai-contrib/jupyter-server-mcp) |
| Optional server-managed documents | [Jupyter Server Documents](https://github.com/jupyter-ai-contrib/jupyter-server-documents) |
| Connection to external agents | [Jupyter AI ACP client](https://github.com/jupyter-ai-contrib/jupyter-ai-acp-client) |

Follow one technical choice from a GitHub discussion to code or a release. For example, [Jupyter AI's external-agent design discussion](https://github.com/jupyterlab/jupyter-ai/issues/1531) shows why maintainers considered connecting existing agents. **Optional:** spend 5–10 minutes reading that issue and looking for the corresponding release change; no account or installation is needed.

### The Eye

A brief look at a current story from Project Jupyter. The article and evidence links are collected below for reading once publication is approved.

## Around 3:45 - Second half: Your questions and projects

Stay for optional small-group and individual discussion and help. What are you trying to do? Bring a question, start something, or get help making progress on work you have already begun. You are welcome to revisit today's example, but this is not a continuation of the prepared demonstration. No project, installation or student account is required.

## Session resources

**Demonstration materials (pending acceptance and publication review):** [Starter notebook](minimal-chat.ipynb) · [Disposable demo notebook](demo.ipynb) · [Three-stage companion](companion.md) · [Model/API](images/stage1-model-api.svg), [MCP](images/stage2-mcp.svg) and [ACP](images/stage3-acp.svg) diagrams. The prepared demonstration is instructor-led; watching or reading requires no installation, account or access to the instructor's model.

**The Eye and supporting evidence (after the session and separate publication approval):** [The Eye — Week 3](the-eye.md) · [Research and primary sources](research.md) · [AI software timeline](images/ai-timeline.svg) · [Origins graphic](images/origin-inventory.svg). These links refer to the working Week 3 files; their appearance here is not approval for public release.

When running any AI-assisted example independently, review its tools and permissions, use disposable files and compare the result with the original notebook rather than trusting the assistant's description.

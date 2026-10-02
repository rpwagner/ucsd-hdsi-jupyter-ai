# Week 3 Agenda

> [!WARNING]
> **Trust but verify.** Even examples Rick shares and AI-generated suggestions can be wrong or unsafe. Read code, commands and configuration before running them; use disposable copies, keep backups, and check what files and tools an agent can access. Don't let an example eat your homework.

**Jupyter AI on your laptop**<br>
**Thursday, October 15, 2026 | 3:00-4:30 PM**<br>
**HDSI, Room 210 | UC San Diego local time**

*Planned deployment sequence; the persona, model/provider, package versions and agent integration will be selected and tested before the session.*

## 3:00 - First half: Give a notebook an AI collaborator

### Intro and Recap

Reconnect the notebook, server and kernel from Week 2. This time we will add AI to that laptop deployment and inspect what changes when an assistant can use notebook tools rather than only produce an answer.

### Start with a persona, the MCP server and Jupyter Server Documents

Begin with a prepared [Jupyter AI](https://jupyter-ai.readthedocs.io/en/stable/users/) setup: a simple model-backed persona, the [Jupyter MCP server](https://github.com/jupyter-ai-contrib/jupyter-server-mcp), and [Jupyter Server Documents (JSD)](https://github.com/jupyter-ai-contrib/jupyter-server-documents). We will use a disposable notebook to inspect a cell, request one small change, review the proposed action, and check the resulting document and output.

Follow the request through the chat, persona, model interaction, MCP tool call and document/kernel operation. Identify which component produces a suggestion, which requests an action, and which changes the notebook or executes code. Compare the state visible in the browser with the server-managed document and the kernel's live variables.

JSD is a deliberate choice for this teaching deployment, not a claim that every Jupyter AI installation requires it. The [Jupyter AI release notes](https://jupyter-ai.readthedocs.io/en/stable/releases/v3.2.0.html) describe it as an optional integration; we will validate the selected combination before providing setup instructions.

### Add an agent and compare the deployment

Next, add [Goose](https://block.github.io/goose/) or another compatible external agent to the same example. Repeat the small notebook task and inspect where the model-and-tool loop now runs, how the agent reaches the notebook tools, and what access it has. Use the [Agent Client Protocol integration](https://github.com/jupyter-ai-contrib/jupyter-ai-acp-client) to distinguish the chat-to-agent connection from MCP's tool interface, rather than treating persona, model, agent and tool server as interchangeable names.

We may containerize this Week 3 example to make the environment disposable and its access easier to control. Before running it, inspect any mounted directories, credentials, network access and enabled tools. A container does not protect homework that has been made accessible to the agent. Containerization remains a preparation decision, not a safety guarantee or a requirement to install anything during the session.

### Map the added pieces to their code and review process

| Piece we add | Repository to inspect |
| --- | --- |
| Jupyter AI chat and persona integration | [jupyterlab/jupyter-ai](https://github.com/jupyterlab/jupyter-ai) |
| MCP tool interface | [jupyter-ai-contrib/jupyter-server-mcp](https://github.com/jupyter-ai-contrib/jupyter-server-mcp) |
| Server-managed documents | [jupyter-ai-contrib/jupyter-server-documents](https://github.com/jupyter-ai-contrib/jupyter-server-documents) |
| External-agent connection | [jupyter-ai-contrib/jupyter-ai-acp-client](https://github.com/jupyter-ai-contrib/jupyter-ai-acp-client) |

Follow an integration or permission question into documentation, an issue, a test or a pull request. The selected agent and tool-provider packages will also be mapped to their repositories when the demonstration is assembled. We are using the deployment to understand both the software boundaries and the open-source work needed to make the pieces cooperate.

### The Eye

A brief look at a current story from Project Jupyter, with the article shared for reading afterward.

## Around 3:45 - Second half: Your questions and projects

Stay for optional small-group and individual discussion and help. What are you trying to do? Bring a question, start something, or get help making progress on work you have already begun. You are welcome to revisit today's example, but this is not a continuation of the prepared demonstration. No project or installation is required.

## Session resources

**Preparation still to come:** the working example, package requirements, model/provider and any credential or cost requirements, access controls, reset instructions, and the decision about containerization. A prepared demonstration and repository exploration will remain available without requiring students to connect personal files or accounts.

When using the example independently, compare any changed notebook with the original rather than relying on the assistant's claim that it succeeded.

**Optional references:** [Jupyter AI user guide](https://jupyter-ai.readthedocs.io/en/stable/users/) · [Jupyter Server Documents](https://github.com/jupyter-ai-contrib/jupyter-server-documents) · [Jupyter MCP server](https://github.com/jupyter-ai-contrib/jupyter-server-mcp) · [Goose](https://block.github.io/goose/).

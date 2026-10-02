# Week 4 Agenda

> [!WARNING]
> **Trust but verify.** Even examples Rick shares and AI-generated suggestions can be wrong or unsafe. Read code, commands and configuration before running them; use disposable copies, keep backups, and check what files and tools an agent can access. Don't let an example eat your homework.

**Jupyter in education: the DataHub deployment**<br>
**Thursday, October 22, 2026 | 3:00-4:30 PM**<br>
**HDSI, Room 210 | UC San Diego local time**

*Planned outline; deployment details and examples will be verified before the session.*

## 3:00 - First half: Trace a notebook through a teaching service

### Intro and Recap

Get settled and carry forward what we learned from the laptop and AI-enabled deployments. Which components would need to change when many students use a shared service?

### Use DataHub to find the boundaries

Use a small notebook example in [UC San Diego DataHub](https://datahub.ucsd.edu/) to investigate the path from a browser session to a user's server, Python environment and kernel. Compare the visible components with the laptop case, then trace the roles of authentication, JupyterHub and the infrastructure running the environment. We will distinguish what we can observe from deployment details that need documentation or confirmation.

Map the selected components to [JupyterHub's repository](https://github.com/jupyterhub/jupyterhub) and the relevant upstream software and deployment configuration. Use a configuration choice or behavior we encounter to find its documentation, an issue or a proposed change. The goal is to understand how a university assembles Jupyter software and how experience using it can become useful upstream feedback.

[Data 8](https://data8.org/) is a possible further example for inspecting how teaching materials and notebook environments are developed and shared. Education supplies the use case; the deployment and its open-source process remain what we investigate.

### The Eye

A brief look at a current story from Project Jupyter, with the article shared for reading afterward.

## Around 3:45 - Second half: Your questions and projects

Stay for optional small-group and individual discussion and help. What are you trying to do? Bring a question, start something, or get help making progress on work you have already begun. You are welcome to revisit today's example, but this is not a continuation of the prepared demonstration. No project or installation is required.

## Session resources

For independent exploration, use disposable examples rather than changing a shared service or course environment. Repository exploration and conversation require no new installation.

**Optional references:** [UC San Diego DataHub/DSMLP guide](https://edtech.ucsd.edu/instructional-tools/dsmlp-datahub/index.html) · [JupyterHub documentation](https://jupyterhub.readthedocs.io/en/stable/) · [JupyterHub on GitHub](https://github.com/jupyterhub/jupyterhub) · [Data 8 on GitHub](https://github.com/data-8).

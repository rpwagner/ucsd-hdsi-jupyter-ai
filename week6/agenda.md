# Week 6 Agenda

> [!WARNING]
> **Trust but verify.** Even examples Rick shares and AI-generated suggestions can be wrong or unsafe. Read code, commands and configuration before running them; use disposable copies, keep backups, and check what files and tools an agent can access. Don't let an example eat your homework.

**Jupyter in business: browser and hosted deployments**<br>
**Thursday, November 5, 2026 | 3:00-4:30 PM**<br>
**HDSI, Room 210 | UC San Diego local time**

*Planned outline; deployment details and company examples will be verified before the session.*

## 3:00 - First half: Run Jupyter in a browser; inspect a hosted product

### Intro and Recap

Get settled and compare the laptop, AI-enabled, classroom and research cases. What can we learn by moving the boundary again?

### Run a small example and locate the implementation

Use a disposable [JupyterLite](https://jupyterlite.readthedocs.io/en/stable/) notebook to investigate where its interface, kernel and data live. Compare what happens when a cell runs with the earlier deployments, then map the implementation to the [JupyterLite repository](https://github.com/jupyterlite/jupyterlite). Use a behavior or limitation we encounter to find documentation, an issue or a change under review.

Next, examine publicly documented company or cloud-provider deployments, with AWS and Bloomberg as possible examples. Identify which Jupyter components we can verify, what the company adds or operates, and where its work meets the upstream projects. These are separate deployment cases, not claims that those services use JupyterLite or share its architecture.

The business lens is practical: use the deployment evidence to understand the software, the product built around it, and the open-source process connecting users, companies and maintainers. We will leave undocumented architectural details as unknown rather than inventing them.

### The Eye

A brief look at a current story from Project Jupyter, with the article shared for reading afterward.

## Around 3:45 - Second half: Your questions and projects

Stay for optional small-group and individual discussion and help. What are you trying to do? Bring a question, start something, or get help making progress on work you have already begun. You are welcome to revisit today's example, but this is not a continuation of the prepared demonstration. No project or installation is required.

## Session resources

Do not put sensitive data into an unfamiliar hosted service. No commercial account or purchase is required to participate.

**Optional references:** [JupyterLite documentation](https://jupyterlite.readthedocs.io/en/stable/) · [JupyterLite on GitHub](https://github.com/jupyterlite/jupyterlite) · [AWS SageMaker JupyterLab](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-jl.html) · [Bloomberg BQuant overview](https://www.bloomberg.com/professional/insights/webinar/introducing-bloombergs-new-quant-platform-for-sell-side-bquant/).

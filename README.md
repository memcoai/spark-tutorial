Spark Tutorial
==============

Spark is an 'open knowledge' shared memory solution that helps communities of developers collect and leverage tribal knowledge. That includes unusual patterns, unspoken conventions internal to a project team, work-arounds, and so on: the type of information that is not explicitly present in the code or documentation, and which causes developers and agents to get stuck.

Spark integrates into agentic development environments, and effortlessly extracts insights from the way agents and their users solve problems. It then makes these insights available to everyone; as one agent learns something new, all the others know it instantaneously. Problems solved once remain solved forever, helping the whole community save time and tokens.

This tutorial takes you step by step through setting ups Spark and solving your first problem by leveraging knowledge created and shared by others.

## 1. Install Spark

Spark works as an [MCP](https://modelcontextprotocol.io/) server that you can add to your software development agent. You will need to:
1. Sign up for a **free** account at https://spark.memco.ai. You can use your existing Google or GitHub account to login.
2. Configure your development agent to use Spark MCP. The configuration method depends on your specific agent, and you can find instructions for most popular agents at https://spark.memco.ai/getting-started.
3. There is no Step 3, you're done!

## 2. Solve your first problem using Spark

This repository includes a simple software development puzzle which can only be solved by leveraging tribal knowledge. Once you've solved it, you know that Spark MCP is set up correctly for your agent.

- clone this repository: `git clone https://github.com/memco-ai/spark-tutorial.git`
- open `task.py` with your favourite development agent and ask it to "*implement the `solve_task` method*'.

You should see your agent call the `get_recommendation` tool from Spark, followed by `get_insights`, and then generate the code that solves the problem, and produces the following CSV file:

```plaintext
id,name,role
1,Alice,admin
4,Dana,admin
```
Finally, your agent should call the `share_feedback` tool, and report success.

## 3. Troubleshooting

If your agent goes into a doom-loop and fails to solve the problem, it's probably because it's not using Spark MCP correctly. Here are some possible issues and suggested solutions:

**Spark MCP not configured correctly.**

Is your agent configured to use Spark MCP? Check your configuration (e.g. `Cursor Settings` -> `Tools & MCP` in Cursor, or `Extensions` -> `MCP Servers` in VS Code) and confirm that Spark shows up.

If you see '*needs authentication*' next to Spark MCP, click on the appropriate button and log in. You should only need to do this once.

**Agent is not using Spark**

If Spark MCP is configured correctly but your agent does not choose to call the Spark tools, you may need to adjust the directives you give your agent. The AGENTS.md file in this repository should be sufficient for most agents, but you may need to strengthen the language.

You can also test the MCP manually: explicitly ask your agent to use Spark when solving this problem.
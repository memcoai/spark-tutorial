Spark Tutorial
==============

Spark is an 'open knowledge' shared memory solution that helps communities of developers collect and leverage tribal knowledge. That includes unusual patterns, unspoken conventions internal to a project team, work-arounds, and so on: the type of information that is not explicitly present in the code or documentation, and which causes developers and agents to get stuck.

Spark integrates with your code development agent (as an MCP server) to:
- surface community-collected insights when your agent gets stuck,
- effortlessly collect insights from your agent when it solves problems, and share those with the community, and
- automatically provide feedback to the community about which insights work and which don't.

As one agent learns something new, all the others know it instantaneously. Problems solved once remain solved forever, helping everybody save time and tokens.

This tutorial takes you step by step through setting ups Spark and solving your first problem by leveraging knowledge created and shared by others.

## 1. Scene setting

This repository includes a simple software development puzzle which can only be solved by leveraging tribal knowledge. There are many kinds of tribal knowledge: API quirks, unwritten conventions without which the code fails, details missing from the documentation, etc. For this example, we use a simple mock Python library called `slothframe` which purports to do optimised data processing, with enterprise grade security. For development mode, there is a secret password that avoids having to use the corporate login server, but that default passwords is not documented (because everyone knows it, right?).

To get started, clone this repository: `git clone https://github.com/memco-ai/spark-tutorial.git` so you have a local copy of the code.

Create a project for your favorite development agent pointing at the newly checkout out directory (`spark-tutorial`), open the `task.py` file, and prompt it to "*implement the `solve_task` method*'.

Most agents should have mo problem generating the code to solve that problem, but they will fail to complete the task because they are unable to guess the development mode password. Feel free to interrupt the doom-loop of failed attempts once you've convinced yourself it's not going to work 😃.

At this point you would normally reach for forums about SlothFrame, or ask your colleagues. But instead, let's use Spark to solve the problem.

## 2. Install Spark

Spark works as an [MCP](https://modelcontextprotocol.io/) server that you can add to your software development agent. You will need to:
1. Sign up for a **free** account at https://spark.memco.ai. You can use your existing Google or GitHub account to login.
2. Configure your development agent to use Spark MCP. The configuration method depends on your specific agent, and you can find instructions for most popular agents at https://spark.memco.ai/.
3. There is no Step 3, you're done!

## 2. Solve your first problem using Spark

Now that you have Spark installed and enabled, let's try to solve the problem from Step 1 again. Revert any changes made, and ask your agent again to implement the `solve_task` method.

This time, you should see your agent call the `get_recommendation` tool from Spark, followed by `get_insights`, and then generate the code that solves the problem, and produces the following CSV file:

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
# Demo Walkthrough

## What To Show

This demo shows an agent moving through a graph-based workflow:

1. Receive a task.
2. Plan whether a tool is needed.
3. Select a tool call.
4. Execute the tool through a registry.
5. Return a structured answer.
6. Inspect execution memory and evaluation reports.

## Suggested Interview Demos

Calculation:

```text
Calculate 24 * 7 + 13
```

Expected behavior:

- The local planner selects the calculator tool.
- The tool registry executes the calculator.
- The app returns the plan, tool call, and result.

Summarization:

```text
Summarize: Agents can plan tasks, call tools, and return structured results.
```

Todo extraction:

```text
Create todos from: read the README, run the tests, deploy the app
```

## What This Proves

- I understand the difference between a chatbot and a tool-using agent.
- I can structure agent execution as a graph with LangGraph.
- I can test agent behavior without relying on paid API calls.
- I can expose optional OpenAI planning while keeping a deterministic local fallback.
- I can evaluate agent behavior with tool-selection, trajectory, error-recovery, latency, and execution-log checks.

## 60-90 Second Walkthrough Script

This is the interview-ready version:

1. "This is a LangGraph-style AI Agent Assistant. The goal is to show the difference between a chatbot and an agent: the agent can plan, select tools, execute them, remember what happened, and return a structured response."
2. "The architecture is `plan -> act -> remember -> respond`. The deterministic local planner keeps the demo and CI reproducible, while the OpenAI planner can be enabled with an API key."
3. "For a calculation task like `Calculate 24 * 7 + 13`, the planner selects the calculator tool, the registry executes it, and the UI shows the plan, tool call, result, execution memory, and answer."
4. "Tool failures are handled deliberately. A task like `Calculate 10 / 0` returns a structured tool error instead of crashing the graph."
5. "The v0.3.0 evaluation suite checks tool selection accuracy, graph trajectory, answer terms, error recovery, and latency, then writes Markdown and JSON reports for regression testing."
6. "This project proves I can build, test, deploy, document, and explain a small but production-minded AI agent system."

## Video Asset

[Watch the 63-second walkthrough video](video/agent-assistant-walkthrough.mp4)

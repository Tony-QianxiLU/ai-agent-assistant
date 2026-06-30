# Demo Walkthrough

## What To Show

This demo shows an agent moving through a graph-based workflow:

1. Receive a task.
2. Plan whether a tool is needed.
3. Select a tool call.
4. Execute the tool through a registry.
5. Return a structured answer.

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


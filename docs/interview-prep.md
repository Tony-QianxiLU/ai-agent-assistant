# Interview Preparation

## Recruiter-Friendly Explanation

AI Agent Assistant is a deployed GenAI application that demonstrates tool-using agent behavior. It plans a task, selects tools, executes them, records execution memory, handles tool failures, evaluates behavior, and returns a structured response.

In simple terms: a chatbot mostly replies with text, while this agent can decide whether a tool is needed, call that tool, show what happened, and recover from tool errors without crashing.

## Technical Questions

| Question | Strong answer points |
| --- | --- |
| What makes this an agent instead of a chatbot? | It has a planning step, tool selection, tool execution, memory, and a structured response path. |
| Why use a graph workflow? | The graph makes execution explicit: plan, act, remember, respond. That improves testability and explainability. |
| Why use a local deterministic planner? | It keeps demos and CI stable without requiring paid API calls, while still allowing optional OpenAI planning. |
| How are tool failures handled? | ToolRegistry catches exceptions and returns structured error results, so the graph can continue and explain the failure. |
| What does the evaluation suite measure? | Tool selection accuracy, graph trajectory, answer terms, error recovery, overall pass rate, latency, and execution logs. |
| What is execution memory? | A lightweight trace of task, plan, and tool results that helps users and developers inspect what happened. |

## Architecture Questions

| Question | Strong answer points |
| --- | --- |
| Why separate planner, graph, tools, and memory? | Each part has a clear responsibility and can be tested independently. |
| How does the tool registry help? | It decouples tool implementation from orchestration and centralizes error isolation. |
| Why expose execution logs? | Logs make behavior inspectable, support debugging, and help evaluate trajectory quality. |
| What is the tradeoff of deterministic planning? | It is reliable and testable but less flexible than LLM planning; optional OpenAI planning can add flexibility later. |

## System Design Questions

| Question | Strong answer points |
| --- | --- |
| How would you make this enterprise-ready? | Add auth, persistent memory, tool permissioning, audit logs, human approval gates, monitoring, and deployment automation. |
| How would you add a web-search tool safely? | Use allowlisted tools, rate limits, source attribution, structured outputs, and human approval for sensitive actions. |
| How would you evaluate an LLM planner? | Use curated tasks, expected tool calls, trajectory checks, regression tests, and optional LLM-as-judge for qualitative outputs. |
| How would you prevent unsafe tool use? | Add tool schemas, input validation, permission checks, approval gates, and sandboxing for risky operations. |

## STAR Stories

### Building a Tool-Using Agent

- Situation: I needed a portfolio project that showed agent orchestration, not just chat completion.
- Task: Build an assistant that can plan, call tools, record memory, and return structured responses.
- Action: I implemented a LangGraph-style workflow with planner, tool registry, memory, and response nodes.
- Result: The project now has a live demo, 19 passing tests, CI, v0.3.0 evaluation reports, screenshots, GIF, and walkthrough video.

### Handling Tool Errors

- Situation: Tool calls can fail in real agent systems.
- Task: Make tool failures visible without crashing the app.
- Action: I wrapped tool execution in the registry and returned structured success/error results.
- Result: The agent can show `calculator (error): Tool error...`, and the evaluation suite verifies error recovery.

### Adding Agent Evaluation

- Situation: Agent demos can look impressive but hide brittle behavior.
- Task: Add an offline benchmark for planning, trajectory, and error recovery.
- Action: I created JSONL eval cases for calculator, summarizer, todo extraction, no-tool response, and divide-by-zero recovery.
- Result: The benchmark passes 5/5 cases and writes Markdown/JSON reports with structured execution logs.

## Common Follow-Up Questions

- How would you add more tools?
- How would you evaluate a multi-step agent?
- How would you store memory across sessions?
- How would you prevent tools from taking unsafe actions?
- How would you debug a bad tool selection?
- What would you change before using this in production?

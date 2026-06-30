# Evaluation

This project includes an offline AI agent evaluation suite that runs without paid API calls.

The goal is to make the agent interview-ready by showing not only that it can run a few tasks, but also that planning, tool selection, graph trajectory, error recovery, and execution logging can be measured after code, prompt, or model changes.

## What It Measures

| Metric | Meaning |
| --- | --- |
| Tool selection accuracy | Whether the planner selected the expected tool names for each task. |
| Trajectory accuracy | Whether graph memory recorded the expected execution path, such as task, plan, and tool steps. |
| Answer terms rate | Whether the final answer includes expected output terms. |
| Error recovery rate | Whether expected tool errors are isolated and exposed without crashing the graph. |
| Overall pass rate | Whether a case passes all evaluation checks together. |
| Average latency | How long each benchmark task takes to run locally. |

## Benchmark Dataset

The benchmark lives in:

```text
data/evaluation_cases.jsonl
```

Each JSONL row includes:

- `id`
- `task`
- `expected_tools`
- `expected_answer_terms`
- `expected_memory_steps`
- `expected_error`

The current dataset covers:

- Calculator tool selection
- Summarizer tool selection
- Todo extractor tool selection
- Direct no-tool response trajectory
- Tool error recovery

## Run Evaluation

```bash
PYTHONPATH=src uv run agent-evaluate
```

Generated reports:

```text
reports/evaluation-report.md
reports/evaluation-report.json
```

## Current Result

| Metric | Result |
| --- | ---: |
| Tool selection accuracy | 100% |
| Trajectory accuracy | 100% |
| Answer terms rate | 100% |
| Error recovery rate | 100% |
| Overall pass rate | 100% |

See [reports/evaluation-report.md](../reports/evaluation-report.md) for case-level details and structured execution logs.

## CI Integration

GitHub Actions runs the evaluation suite after linting and tests:

```bash
PYTHONPATH=src uv run agent-evaluate
```

This means changes to planning, tool execution, graph state, memory, or response rendering are checked automatically on push and pull request.

## Future Improvements

- Add LLM planner eval cases when an OpenAI API key is configured.
- Track latency trends over time.
- Add task difficulty tiers.
- Add optional LLM-as-judge scoring for answer helpfulness.
- Store generated reports as CI artifacts.

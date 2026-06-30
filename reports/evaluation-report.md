# Agent Evaluation Report

## Summary

- Total cases: 5
- Passed cases: 5
- Tool selection accuracy: 100%
- Trajectory accuracy: 100%
- Answer terms rate: 100%
- Error recovery rate: 100%
- Overall pass rate: 100%
- Average latency: 0.9 ms

## Case Results

| Case | Tool selection | Trajectory | Answer terms | Error recovery | Latency | Expected tools | Selected tools |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| calculator-tool-selection | PASS | PASS | PASS | PASS | 1.9 ms | calculator | calculator |
| summarizer-tool-selection | PASS | PASS | PASS | PASS | 0.7 ms | summarizer | summarizer |
| todo-tool-selection | PASS | PASS | PASS | PASS | 0.6 ms | todo_extractor | todo_extractor |
| direct-response-trajectory | PASS | PASS | PASS | PASS | 0.5 ms | None | None |
| tool-error-recovery | PASS | PASS | PASS | PASS | 0.5 ms | calculator | calculator |

## Execution Logs

### calculator-tool-selection

```json
[
  {
    "type": "memory",
    "step": "task",
    "content": "Calculate 24 * 7 + 13"
  },
  {
    "type": "memory",
    "step": "plan",
    "content": "The task contains an arithmetic expression, so I will use the calculator."
  },
  {
    "type": "memory",
    "step": "tool:calculator",
    "content": "success - 181"
  },
  {
    "type": "tool_result",
    "name": "calculator",
    "success": true,
    "output": "181"
  },
  {
    "type": "answer",
    "content": "Plan: The task contains an arithmetic expression, so I will use the calculator.\n\nTool results:\ncalculator (ok): 181"
  }
]
```

### summarizer-tool-selection

```json
[
  {
    "type": "memory",
    "step": "task",
    "content": "Summarize: Agents can plan tasks. They can call tools and return structured results."
  },
  {
    "type": "memory",
    "step": "plan",
    "content": "The task asks for a summary, so I will use the summarizer."
  },
  {
    "type": "memory",
    "step": "tool:summarizer",
    "content": "success - Agents can plan tasks."
  },
  {
    "type": "tool_result",
    "name": "summarizer",
    "success": true,
    "output": "Agents can plan tasks."
  },
  {
    "type": "answer",
    "content": "Plan: The task asks for a summary, so I will use the summarizer.\n\nTool results:\nsummarizer (ok): Agents can plan tasks."
  }
]
```

### todo-tool-selection

```json
[
  {
    "type": "memory",
    "step": "task",
    "content": "Create todos from: read the README, run the tests, deploy the app"
  },
  {
    "type": "memory",
    "step": "plan",
    "content": "The task asks for structured todos, so I will use the todo extractor."
  },
  {
    "type": "memory",
    "step": "tool:todo_extractor",
    "content": "success - - [ ] read the README\n- [ ] run the tests\n- [ ] deploy the app"
  },
  {
    "type": "tool_result",
    "name": "todo_extractor",
    "success": true,
    "output": "- [ ] read the README\n- [ ] run the tests\n- [ ] deploy the app"
  },
  {
    "type": "answer",
    "content": "Plan: The task asks for structured todos, so I will use the todo extractor.\n\nTool results:\ntodo_extractor (ok): - [ ] read the README\n- [ ] run the tests\n- [ ] deploy the app"
  }
]
```

### direct-response-trajectory

```json
[
  {
    "type": "memory",
    "step": "task",
    "content": "Hello agent"
  },
  {
    "type": "memory",
    "step": "plan",
    "content": "No tool is required. I will answer directly with a clarification."
  },
  {
    "type": "answer",
    "content": "I did not need to call a tool. Try a calculation, summarization, or todo extraction task."
  }
]
```

### tool-error-recovery

```json
[
  {
    "type": "memory",
    "step": "task",
    "content": "Calculate 10 / 0"
  },
  {
    "type": "memory",
    "step": "plan",
    "content": "The task contains an arithmetic expression, so I will use the calculator."
  },
  {
    "type": "memory",
    "step": "tool:calculator",
    "content": "failed - Tool error: float division by zero"
  },
  {
    "type": "tool_result",
    "name": "calculator",
    "success": false,
    "output": "Tool error: float division by zero"
  },
  {
    "type": "answer",
    "content": "Plan: The task contains an arithmetic expression, so I will use the calculator.\n\nTool results:\ncalculator (error): Tool error: float division by zero"
  }
]
```

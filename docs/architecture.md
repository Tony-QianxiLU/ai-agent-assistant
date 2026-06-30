# Architecture

## Goal

The goal of this project is to build a practical agent assistant that can plan a task, select tools, execute them, and return a structured result.

## Workflow

1. User enters a task.
2. Planner decides whether tools are needed.
3. LangGraph routes execution through plan, act, and respond nodes.
4. Tool registry executes selected tools.
5. Assistant returns plan, tool calls, and result.

## Design Choices

- The local deterministic planner makes the app runnable without API keys.
- The OpenAI planner is optional and can be enabled through environment variables.
- Tool functions are small and independently testable.
- LangGraph makes the execution flow explicit.


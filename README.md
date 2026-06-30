# AI Agent Assistant

An AI assistant that can plan a task, call tools, and return a structured result.

This repository is part of my AI engineering portfolio. It demonstrates practical agent engineering concepts: task planning, tool calling, graph-based execution, testing, documentation, and optional LLM integration.

## Current Status

Phase 1: portfolio-ready local agent prototype.

The current version includes:

- LangGraph workflow
- Local deterministic planner
- Optional OpenAI planner
- Tool registry
- Calculator tool
- Text summarizer tool
- Todo extraction tool
- Streamlit UI
- Tests and CI
- Deployment notes

## Screenshot

![AI Agent Assistant Streamlit UI](docs/assets/streamlit-home.png)

## Architecture

```text
User task
   |
   v
Planner
   |
   v
Tool calls
   |
   v
Tool registry
   |
   v
Tool results
   |
   v
Final response
```

## Tech Stack

- Python 3.12
- LangGraph
- LangChain OpenAI
- Streamlit
- pytest
- ruff
- uv

## Getting Started

Install dependencies:

```bash
uv sync
```

Run the app:

```bash
uv run streamlit run src/ai_agent_assistant/app.py
```

Run tests:

```bash
uv run ruff check .
uv run pytest
```

## Example Tasks

```text
Calculate 24 * 7 + 13
```

```text
Summarize: Retrieval augmented generation combines search with generation.
```

```text
Create todos from: read the README, run the tests, deploy the app
```

## Environment Variables

Copy `.env.example` to `.env` if you want to use OpenAI planning:

```bash
cp .env.example .env
```

Never commit real API keys.

## Roadmap

- [x] Create professional project skeleton
- [x] Add LangGraph workflow
- [x] Add local planner
- [x] Add tool registry
- [x] Add calculator, summarizer, and todo tools
- [x] Add Streamlit UI
- [x] Add tests
- [x] Add CI
- [x] Add optional OpenAI planner
- [ ] Add persistent memory
- [ ] Add browser/search tool
- [ ] Deploy public demo

## Interview Talking Points

This project is designed to demonstrate:

- How agents differ from simple chatbots
- How tool calling works
- Why deterministic local fallbacks are useful
- How LangGraph structures multi-step workflows
- How to test agent behavior without relying on external API calls


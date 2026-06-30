# Contributing

Thanks for your interest in improving AI Agent Assistant.

## Development Setup

```bash
uv sync
PYTHONPATH=src uv run streamlit run src/ai_agent_assistant/app.py
```

## Quality Checks

Run these before opening a pull request:

```bash
uv run ruff check .
uv run pytest
```

## Pull Request Guidelines

- Keep changes focused and easy to review.
- Add or update tests for behavior changes.
- Update documentation when user-facing behavior changes.
- Do not commit real API keys, `.env` files, private prompts, or private task data.

## Project Priorities

- Clear agent workflow design.
- Deterministic tests without paid API calls.
- Safe tool execution and explicit failure handling.
- Human approval before risky tools are added.

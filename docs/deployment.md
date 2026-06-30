# Deployment

## Local

```bash
uv run streamlit run src/ai_agent_assistant/app.py
```

## Streamlit Community Cloud

Suggested settings:

- Main file path: `src/ai_agent_assistant/app.py`
- Python version: `3.12`
- Secrets:
  - `OPENAI_API_KEY`
  - `OPENAI_MODEL`

## Production Considerations

- Store secrets in the deployment platform's secret manager.
- Add human approval for tools that can send messages, spend money, delete files, or access private systems.
- Log tool calls for auditability.
- Add evaluation cases for agent plans and tool results.


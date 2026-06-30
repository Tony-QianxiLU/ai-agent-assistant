# Deployment

## Live URL

<https://tony-qianxilu-ai-agent-assistant.streamlit.app/>

## Local

```bash
uv sync
PYTHONPATH=src uv run streamlit run src/ai_agent_assistant/app.py
```

## Streamlit Community Cloud

Use the public GitHub repository:

- Repository: `Tony-QianxiLU/ai-agent-assistant`
- Branch: `main`
- Main file path: `src/ai_agent_assistant/app.py`
- Python version: `3.12`

Optional secrets:

```toml
OPENAI_API_KEY = "..."
OPENAI_MODEL = "gpt-4.1-mini"
```

## Production Considerations

- Store secrets only in the deployment platform's secret manager.
- Add approval gates for tools that send messages, spend money, mutate data, or access private systems.
- Log tool calls and tool results for auditability.
- Add planner and tool evaluation datasets before expanding tool coverage.
- Persist memory only after defining privacy and retention requirements.

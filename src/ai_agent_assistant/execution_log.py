from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def state_to_execution_log(state: Mapping[str, Any]) -> list[dict[str, object]]:
    """Render graph state as a structured execution log for reports and debugging."""
    entries: list[dict[str, object]] = []

    for memory in state.get("memory", []):
        entries.append(
            {
                "type": "memory",
                "step": memory.step,
                "content": memory.content,
            }
        )

    for result in state.get("tool_results", []):
        entries.append(
            {
                "type": "tool_result",
                "name": result.name,
                "success": result.success,
                "output": result.output,
            }
        )

    answer = state.get("answer")
    if answer:
        entries.append(
            {
                "type": "answer",
                "content": str(answer),
            }
        )

    return entries

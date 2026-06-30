import json
import re
from dataclasses import dataclass

from langchain_openai import ChatOpenAI

from ai_agent_assistant.tools import ToolCall


@dataclass(frozen=True)
class Plan:
    reasoning: str
    tool_calls: list[ToolCall]


class LocalPlanner:
    def plan(self, task: str) -> Plan:
        normalized = task.strip()
        lower_task = normalized.lower()

        if not normalized:
            return Plan(reasoning="No task was provided.", tool_calls=[])

        if "calculate" in lower_task or re.search(r"\d+\s*[-+*/%]\s*\d+", normalized):
            expression = _extract_expression(normalized)
            return Plan(
                reasoning="The task contains an arithmetic expression, so I will use the calculator.",
                tool_calls=[ToolCall(name="calculator", arguments={"expression": expression})],
            )

        if lower_task.startswith("summarize:") or "summarize" in lower_task:
            text = _extract_after_marker(normalized, "summarize")
            return Plan(
                reasoning="The task asks for a summary, so I will use the summarizer.",
                tool_calls=[ToolCall(name="summarizer", arguments={"text": text})],
            )

        if "todo" in lower_task or "todos" in lower_task:
            text = _extract_after_marker(normalized, "from")
            return Plan(
                reasoning="The task asks for structured todos, so I will use the todo extractor.",
                tool_calls=[ToolCall(name="todo_extractor", arguments={"text": text})],
            )

        return Plan(
            reasoning="No tool is required. I will answer directly with a clarification.",
            tool_calls=[],
        )


class OpenAIPlanner:
    def __init__(self, model: str) -> None:
        self._model = ChatOpenAI(model=model, temperature=0)

    def plan(self, task: str) -> Plan:
        prompt = (
            "You are an agent planner. Choose tool calls for this task. "
            "Available tools: calculator(expression), summarizer(text), todo_extractor(text). "
            "Return strict JSON with keys reasoning and tool_calls. "
            "Each tool call has name and arguments.\n\n"
            f"Task: {task}"
        )
        response = self._model.invoke(prompt)
        data = json.loads(str(response.content))
        return Plan(
            reasoning=str(data.get("reasoning", "")),
            tool_calls=[
                ToolCall(
                    name=str(item["name"]),
                    arguments={str(key): str(value) for key, value in item.get("arguments", {}).items()},
                )
                for item in data.get("tool_calls", [])
            ],
        )


def _extract_expression(task: str) -> str:
    cleaned = task.lower().replace("calculate", "").replace("what is", "")
    allowed = re.findall(r"[0-9+\-*/().% ]+", cleaned)
    expression = "".join(allowed).strip()
    return expression or task


def _extract_after_marker(task: str, marker: str) -> str:
    pattern = re.compile(rf"{marker}\s*:?", re.IGNORECASE)
    parts = pattern.split(task, maxsplit=1)
    if len(parts) == 2 and parts[1].strip():
        return parts[1].strip()
    return task


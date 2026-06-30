from ai_agent_assistant.planner import LocalPlanner


def test_local_planner_selects_calculator() -> None:
    plan = LocalPlanner().plan("Calculate 10 + 5")

    assert plan.tool_calls[0].name == "calculator"
    assert plan.tool_calls[0].arguments["expression"] == "10 + 5"


def test_local_planner_selects_summarizer() -> None:
    plan = LocalPlanner().plan("Summarize: Agents use tools.")

    assert plan.tool_calls[0].name == "summarizer"
    assert plan.tool_calls[0].arguments["text"] == "Agents use tools."


def test_local_planner_selects_todo_extractor() -> None:
    plan = LocalPlanner().plan("Create todos from: read docs, run tests")

    assert plan.tool_calls[0].name == "todo_extractor"
    assert "read docs" in plan.tool_calls[0].arguments["text"]


def test_local_planner_can_choose_no_tool() -> None:
    plan = LocalPlanner().plan("Hello")

    assert plan.tool_calls == []


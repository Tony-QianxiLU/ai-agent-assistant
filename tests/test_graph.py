from ai_agent_assistant.graph import AgentGraph


def test_agent_graph_runs_calculator_tool() -> None:
    result = AgentGraph().invoke("Calculate 3 * 9")

    assert result["plan"].tool_calls[0].name == "calculator"
    assert "27" in result["answer"]


def test_agent_graph_handles_no_tool_task() -> None:
    result = AgentGraph().invoke("Hello")

    assert result["tool_results"] == []
    assert "did not need to call a tool" in result["answer"]


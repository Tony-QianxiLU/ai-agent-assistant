from ai_agent_assistant.tools import ToolCall, calculate, default_registry, extract_todos, summarize


def test_calculate_basic_expression() -> None:
    assert calculate({"expression": "24 * 7 + 13"}) == "181"


def test_calculate_rejects_unsafe_expression() -> None:
    try:
        calculate({"expression": "__import__('os').system('echo unsafe')"})
    except ValueError as error:
        assert "basic arithmetic" in str(error)
    else:
        raise AssertionError("Unsafe expression should fail")


def test_summarize_returns_first_sentence() -> None:
    result = summarize({"text": "Agents can call tools. They can also plan."})

    assert result == "Agents can call tools."


def test_extract_todos_creates_markdown_checklist() -> None:
    result = extract_todos({"text": "read README, run tests and deploy app"})

    assert "- [ ] read README" in result
    assert "- [ ] run tests" in result
    assert "- [ ] deploy app" in result


def test_default_registry_runs_registered_tool() -> None:
    result = default_registry().run(ToolCall(name="calculator", arguments={"expression": "2 + 2"}))

    assert result.output == "4"


def test_default_registry_isolates_tool_errors() -> None:
    result = default_registry().run(
        ToolCall(name="calculator", arguments={"expression": "10 / 0"})
    )

    assert result.success is False
    assert "Tool error" in result.output

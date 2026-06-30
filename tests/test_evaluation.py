from pathlib import Path

from ai_agent_assistant.evaluation import (
    AgentEvaluationCase,
    AgentEvaluationResult,
    evaluate_agent,
    load_evaluation_cases,
    pass_rate_for,
    render_markdown_report,
    write_json_report,
    write_markdown_report,
)


def test_evaluate_agent_scores_tool_selection_trajectory_and_error_recovery() -> None:
    cases = [
        AgentEvaluationCase(
            id="calculator",
            task="Calculate 2 + 2",
            expected_tools=["calculator"],
            expected_answer_terms=["4"],
            expected_memory_steps=["task", "plan", "tool:calculator"],
        ),
        AgentEvaluationCase(
            id="error",
            task="Calculate 10 / 0",
            expected_tools=["calculator"],
            expected_answer_terms=["error", "Tool error"],
            expected_memory_steps=["task", "plan", "tool:calculator"],
            expected_error=True,
        ),
    ]

    report = evaluate_agent(cases)

    assert report.summary.total_cases == 2
    assert report.summary.passed_cases == 2
    assert report.summary.tool_selection_accuracy == 1.0
    assert report.summary.trajectory_accuracy == 1.0
    assert report.summary.error_recovery_rate == 1.0
    assert report.summary.average_latency_ms >= 0.0
    assert all(result.execution_log for result in report.results)


def test_load_evaluation_cases_reads_jsonl() -> None:
    cases = load_evaluation_cases(Path("data/evaluation_cases.jsonl"))

    assert len(cases) == 5
    assert cases[0].id == "calculator-tool-selection"
    assert cases[0].expected_tools == ["calculator"]
    assert cases[-1].expected_error is True


def test_benchmark_cases_pass_current_agent_suite() -> None:
    cases = load_evaluation_cases(Path("data/evaluation_cases.jsonl"))

    report = evaluate_agent(cases)

    assert report.summary.total_cases == 5
    assert report.summary.overall_pass_rate == 1.0
    assert all(result.passed for result in report.results)


def test_render_markdown_report_includes_summary_cases_and_logs() -> None:
    result = AgentEvaluationResult(
        id="case-1",
        task="Calculate 2 + 2",
        expected_tools=["calculator"],
        selected_tools=["calculator"],
        memory_steps=["task", "plan", "tool:calculator"],
        answer="calculator (ok): 4",
        latency_ms=2.5,
        tool_selection_passed=True,
        trajectory_passed=True,
        answer_terms_passed=True,
        error_recovery_passed=True,
        passed=True,
        execution_log=[{"type": "answer", "content": "calculator (ok): 4"}],
    )
    report = evaluate_agent(
        [
            AgentEvaluationCase(
                id="case-1",
                task="Calculate 2 + 2",
                expected_tools=["calculator"],
                expected_answer_terms=["4"],
                expected_memory_steps=["task", "plan", "tool:calculator"],
            )
        ]
    )
    report = type(report)(summary=report.summary, results=[result])

    markdown = render_markdown_report(report)

    assert "# Agent Evaluation Report" in markdown
    assert "Tool selection accuracy" in markdown
    assert "| case-1 | PASS | PASS | PASS | PASS | 2.5 ms | calculator | calculator |" in markdown
    assert "## Execution Logs" in markdown


def test_write_reports_creates_json_and_markdown(tmp_path: Path) -> None:
    cases = load_evaluation_cases(Path("data/evaluation_cases.jsonl"))
    report = evaluate_agent(cases)
    json_path = tmp_path / "report.json"
    markdown_path = tmp_path / "report.md"

    write_json_report(report, json_path)
    write_markdown_report(report, markdown_path)

    assert '"overall_pass_rate": 1.0' in json_path.read_text(encoding="utf-8")
    assert "## Case Results" in markdown_path.read_text(encoding="utf-8")


def test_pass_rate_for_handles_empty_results() -> None:
    assert pass_rate_for([], "tool_selection_passed") == 0.0

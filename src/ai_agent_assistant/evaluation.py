from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean

from ai_agent_assistant.execution_log import state_to_execution_log
from ai_agent_assistant.graph import AgentGraph


@dataclass(frozen=True)
class AgentEvaluationCase:
    id: str
    task: str
    expected_tools: list[str]
    expected_answer_terms: list[str]
    expected_memory_steps: list[str]
    expected_error: bool = False


@dataclass(frozen=True)
class AgentEvaluationResult:
    id: str
    task: str
    expected_tools: list[str]
    selected_tools: list[str]
    memory_steps: list[str]
    answer: str
    latency_ms: float
    tool_selection_passed: bool
    trajectory_passed: bool
    answer_terms_passed: bool
    error_recovery_passed: bool
    passed: bool
    execution_log: list[dict[str, object]]


@dataclass(frozen=True)
class AgentEvaluationSummary:
    total_cases: int
    passed_cases: int
    tool_selection_accuracy: float
    trajectory_accuracy: float
    answer_terms_rate: float
    error_recovery_rate: float
    overall_pass_rate: float
    average_latency_ms: float


@dataclass(frozen=True)
class AgentEvaluationReport:
    summary: AgentEvaluationSummary
    results: list[AgentEvaluationResult]


def load_evaluation_cases(path: Path) -> list[AgentEvaluationCase]:
    cases: list[AgentEvaluationCase] = []
    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue

            payload = json.loads(stripped)
            try:
                cases.append(
                    AgentEvaluationCase(
                        id=payload["id"],
                        task=payload["task"],
                        expected_tools=list(payload["expected_tools"]),
                        expected_answer_terms=list(payload["expected_answer_terms"]),
                        expected_memory_steps=list(payload["expected_memory_steps"]),
                        expected_error=bool(payload.get("expected_error", False)),
                    )
                )
            except KeyError as error:
                raise ValueError(f"Missing required field on line {line_number}: {error}") from error

    return cases


def evaluate_agent(
    cases: list[AgentEvaluationCase],
    graph: AgentGraph | None = None,
) -> AgentEvaluationReport:
    evaluator_graph = graph or AgentGraph()
    results: list[AgentEvaluationResult] = []

    for case in cases:
        started_at = time.perf_counter()
        state = evaluator_graph.invoke(case.task)
        latency_ms = (time.perf_counter() - started_at) * 1000

        plan = state["plan"]
        tool_results = state.get("tool_results", [])
        memory = state.get("memory", [])
        answer = state.get("answer", "")
        selected_tools = [call.name for call in plan.tool_calls]
        memory_steps = [entry.step for entry in memory]
        answer_lower = answer.lower()
        tool_outputs = " ".join(result.output.lower() for result in tool_results)

        tool_selection_passed = selected_tools == case.expected_tools
        trajectory_passed = all(step in memory_steps for step in case.expected_memory_steps)
        answer_terms_passed = all(
            expected_term.lower() in answer_lower for expected_term in case.expected_answer_terms
        )
        error_recovery_passed = _evaluate_error_recovery(
            expected_error=case.expected_error,
            tool_results=tool_results,
            answer_lower=answer_lower,
            tool_outputs=tool_outputs,
        )
        passed = (
            tool_selection_passed
            and trajectory_passed
            and answer_terms_passed
            and error_recovery_passed
        )

        results.append(
            AgentEvaluationResult(
                id=case.id,
                task=case.task,
                expected_tools=case.expected_tools,
                selected_tools=selected_tools,
                memory_steps=memory_steps,
                answer=answer,
                latency_ms=latency_ms,
                tool_selection_passed=tool_selection_passed,
                trajectory_passed=trajectory_passed,
                answer_terms_passed=answer_terms_passed,
                error_recovery_passed=error_recovery_passed,
                passed=passed,
                execution_log=state_to_execution_log(state),
            )
        )

    return AgentEvaluationReport(summary=summarize_results(results), results=results)


def summarize_results(results: list[AgentEvaluationResult]) -> AgentEvaluationSummary:
    total_cases = len(results)
    if total_cases == 0:
        return AgentEvaluationSummary(
            total_cases=0,
            passed_cases=0,
            tool_selection_accuracy=0.0,
            trajectory_accuracy=0.0,
            answer_terms_rate=0.0,
            error_recovery_rate=0.0,
            overall_pass_rate=0.0,
            average_latency_ms=0.0,
        )

    passed_cases = sum(result.passed for result in results)
    return AgentEvaluationSummary(
        total_cases=total_cases,
        passed_cases=passed_cases,
        tool_selection_accuracy=pass_rate_for(results, "tool_selection_passed"),
        trajectory_accuracy=pass_rate_for(results, "trajectory_passed"),
        answer_terms_rate=pass_rate_for(results, "answer_terms_passed"),
        error_recovery_rate=pass_rate_for(results, "error_recovery_passed"),
        overall_pass_rate=passed_cases / total_cases,
        average_latency_ms=mean(result.latency_ms for result in results),
    )


def pass_rate_for(results: list[AgentEvaluationResult], field_name: str) -> float:
    if not results:
        return 0.0

    return sum(bool(getattr(result, field_name)) for result in results) / len(results)


def report_to_dict(report: AgentEvaluationReport) -> dict[str, object]:
    return {
        "summary": asdict(report.summary),
        "results": [asdict(result) for result in report.results],
    }


def write_json_report(report: AgentEvaluationReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report_to_dict(report), indent=2), encoding="utf-8")


def render_markdown_report(report: AgentEvaluationReport) -> str:
    summary = report.summary
    lines = [
        "# Agent Evaluation Report",
        "",
        "## Summary",
        "",
        f"- Total cases: {summary.total_cases}",
        f"- Passed cases: {summary.passed_cases}",
        f"- Tool selection accuracy: {summary.tool_selection_accuracy:.0%}",
        f"- Trajectory accuracy: {summary.trajectory_accuracy:.0%}",
        f"- Answer terms rate: {summary.answer_terms_rate:.0%}",
        f"- Error recovery rate: {summary.error_recovery_rate:.0%}",
        f"- Overall pass rate: {summary.overall_pass_rate:.0%}",
        f"- Average latency: {summary.average_latency_ms:.1f} ms",
        "",
        "## Case Results",
        "",
        (
            "| Case | Tool selection | Trajectory | Answer terms | Error recovery | "
            "Latency | Expected tools | Selected tools |"
        ),
        "| --- | --- | --- | --- | --- | ---: | --- | --- |",
    ]

    for result in report.results:
        lines.append(
            "| "
            f"{result.id} | "
            f"{_format_status(result.tool_selection_passed)} | "
            f"{_format_status(result.trajectory_passed)} | "
            f"{_format_status(result.answer_terms_passed)} | "
            f"{_format_status(result.error_recovery_passed)} | "
            f"{result.latency_ms:.1f} ms | "
            f"{', '.join(result.expected_tools) or 'None'} | "
            f"{', '.join(result.selected_tools) or 'None'} |"
        )

    lines.extend(
        [
            "",
            "## Execution Logs",
            "",
        ]
    )

    for result in report.results:
        lines.append(f"### {result.id}")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(result.execution_log, indent=2))
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def write_markdown_report(report: AgentEvaluationReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_report(report), encoding="utf-8")


def _evaluate_error_recovery(
    *,
    expected_error: bool,
    tool_results: object,
    answer_lower: str,
    tool_outputs: str,
) -> bool:
    results = list(tool_results)
    if expected_error:
        has_error_result = any(not result.success for result in results)
        exposes_error = "error" in answer_lower or "tool error" in tool_outputs
        return has_error_result and exposes_error

    return all(result.success for result in results)


def _format_status(passed: bool) -> str:
    return "PASS" if passed else "FAIL"

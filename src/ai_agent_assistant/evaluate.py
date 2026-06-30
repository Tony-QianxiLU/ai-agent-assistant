from __future__ import annotations

import argparse
from pathlib import Path

from ai_agent_assistant.evaluation import (
    evaluate_agent,
    load_evaluation_cases,
    write_json_report,
    write_markdown_report,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AI agent evaluation benchmark.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path("data/evaluation_cases.jsonl"),
        help="Path to JSONL evaluation cases.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("reports/evaluation-report.json"),
        help="Path for the JSON evaluation report.",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path("reports/evaluation-report.md"),
        help="Path for the Markdown evaluation report.",
    )
    args = parser.parse_args()

    cases = load_evaluation_cases(args.cases)
    report = evaluate_agent(cases)
    write_json_report(report, args.json_output)
    write_markdown_report(report, args.markdown_output)

    summary = report.summary
    print(
        "Evaluation complete: "
        f"{summary.passed_cases}/{summary.total_cases} cases passed, "
        f"tools={summary.tool_selection_accuracy:.0%}, "
        f"trajectory={summary.trajectory_accuracy:.0%}, "
        f"errors={summary.error_recovery_rate:.0%}, "
        f"latency={summary.average_latency_ms:.1f}ms"
    )


if __name__ == "__main__":
    main()

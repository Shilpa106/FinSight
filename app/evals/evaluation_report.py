from app.evals.evaluation_models import EvaluationCaseResult, EvaluationRunSummary


class EvaluationReportGenerator:
    def generate_markdown_report(
        self,
        summary: EvaluationRunSummary,
        results: list[EvaluationCaseResult],
    ) -> str:
        lines: list[str] = []

        lines.append(f"# Evaluation Report: {summary.run_name}")
        lines.append("")
        lines.append(f"Dataset: `{summary.dataset_name}`")
        lines.append("")
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- Total cases: {summary.total_cases}")
        lines.append(f"- Passed cases: {summary.passed_cases}")
        lines.append(f"- Failed cases: {summary.failed_cases}")
        lines.append(f"- Pass rate: {summary.pass_rate:.2%}")
        lines.append(f"- Average retrieval score: {summary.average_retrieval_score:.2f}")
        lines.append(f"- Average answer score: {summary.average_answer_score:.2f}")
        lines.append(f"- Average citation score: {summary.average_citation_score:.2f}")
        lines.append(f"- Average guardrail score: {summary.average_guardrail_score:.2f}")
        lines.append(f"- Average overall score: {summary.average_overall_score:.2f}")
        lines.append("")
        lines.append("## Cases")
        lines.append("")

        for result in results:
            status = "PASS" if result.passed else "FAIL"

            lines.append(f"### {result.case_id} - {status}")
            lines.append("")
            lines.append(f"Question: {result.question}")
            lines.append("")
            lines.append(f"Expected answer: {result.expected_answer}")
            lines.append("")
            lines.append(f"Actual answer: {result.actual_answer}")
            lines.append("")
            lines.append(f"- Retrieval score: {result.retrieval_score:.2f}")
            lines.append(f"- Answer score: {result.answer_score:.2f}")
            lines.append(f"- Citation score: {result.citation_score:.2f}")
            lines.append(f"- Guardrail score: {result.guardrail_score:.2f}")
            lines.append(f"- Overall score: {result.overall_score:.2f}")
            lines.append(f"- Guardrail action: {result.guardrail_action}")
            lines.append(f"- Retrieved chunks: {result.retrieved_chunk_count}")

            if result.error_message:
                lines.append(f"- Error: {result.error_message}")

            lines.append("")

        return "\n".join(lines)
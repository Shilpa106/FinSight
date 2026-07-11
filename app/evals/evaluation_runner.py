from app.evals.evaluation_models import (
    EvaluationCase,
    EvaluationCaseResult,
    EvaluationRunSummary,
)
from app.evals.metrics.answer_metrics import AnswerMetrics
from app.evals.metrics.citation_metrics import CitationMetrics
from app.evals.metrics.guardrail_metrics import GuardrailMetrics
from app.evals.metrics.retrieval_metrics import RetrievalMetrics
from app.services.rag.rag_service import RAGService


class EvaluationRunner:
    def __init__(
        self,
        rag_service: RAGService,
    ) -> None:
        self.rag_service = rag_service
        self.retrieval_metrics = RetrievalMetrics()
        self.answer_metrics = AnswerMetrics()
        self.citation_metrics = CitationMetrics()
        self.guardrail_metrics = GuardrailMetrics()

    def run_case(self, case: EvaluationCase) -> EvaluationCaseResult:
        try:
            rag_result = self.rag_service.answer_question(
                organization_id=case.organization_id,
                user_id=case.user_id,
                document_id=case.document_id,
                question=case.question,
            )

            citations = rag_result.get("citations", [])
            actual_answer = rag_result.get("answer")
            retrieved_chunk_count = rag_result.get("retrieved_chunk_count", 0)
            guardrail_action = rag_result.get("guardrail_action")

            retrieval_score, retrieval_metrics = self.retrieval_metrics.score(
                retrieved_chunk_count=retrieved_chunk_count,
                citations=citations,
                expected_pages=case.expected_pages,
            )

            answer_score, answer_metrics = self.answer_metrics.score(
                actual_answer=actual_answer,
                expected_keywords=case.expected_keywords,
            )

            citation_score, citation_metrics = self.citation_metrics.score(
                citations=citations,
                retrieved_chunk_count=retrieved_chunk_count,
            )

            guardrail_score, guardrail_metrics = self.guardrail_metrics.score(
                should_trigger_guardrail=case.should_trigger_guardrail,
                expected_guardrail_action=case.expected_guardrail_action,
                actual_guardrail_action=guardrail_action,
            )

            overall_score = (
                retrieval_score * 0.30
                + answer_score * 0.30
                + citation_score * 0.20
                + guardrail_score * 0.20
            )

            passed = overall_score >= 0.70

            return EvaluationCaseResult(
                case_id=case.case_id,
                question=case.question,
                expected_answer=case.expected_answer,
                actual_answer=actual_answer,
                citations=citations,
                retrieved_chunk_count=retrieved_chunk_count,
                guardrail_action=guardrail_action,
                retrieval_score=retrieval_score,
                answer_score=answer_score,
                citation_score=citation_score,
                guardrail_score=guardrail_score,
                overall_score=overall_score,
                passed=passed,
                metrics={
                    "retrieval": retrieval_metrics,
                    "answer": answer_metrics,
                    "citation": citation_metrics,
                    "guardrail": guardrail_metrics,
                },
                error_message=None,
            )

        except Exception as error:
            return EvaluationCaseResult(
                case_id=case.case_id,
                question=case.question,
                expected_answer=case.expected_answer,
                actual_answer=None,
                citations=[],
                retrieved_chunk_count=0,
                guardrail_action=None,
                retrieval_score=0.0,
                answer_score=0.0,
                citation_score=0.0,
                guardrail_score=0.0,
                overall_score=0.0,
                passed=False,
                metrics={},
                error_message=str(error),
            )

    def summarize(
        self,
        run_name: str,
        dataset_name: str,
        results: list[EvaluationCaseResult],
    ) -> EvaluationRunSummary:
        total_cases = len(results)
        passed_cases = len([result for result in results if result.passed])
        failed_cases = total_cases - passed_cases

        if total_cases == 0:
            return EvaluationRunSummary(
                run_name=run_name,
                dataset_name=dataset_name,
                total_cases=0,
                passed_cases=0,
                failed_cases=0,
                average_retrieval_score=0.0,
                average_answer_score=0.0,
                average_citation_score=0.0,
                average_guardrail_score=0.0,
                average_overall_score=0.0,
                pass_rate=0.0,
            )

        return EvaluationRunSummary(
            run_name=run_name,
            dataset_name=dataset_name,
            total_cases=total_cases,
            passed_cases=passed_cases,
            failed_cases=failed_cases,
            average_retrieval_score=sum(r.retrieval_score for r in results) / total_cases,
            average_answer_score=sum(r.answer_score for r in results) / total_cases,
            average_citation_score=sum(r.citation_score for r in results) / total_cases,
            average_guardrail_score=sum(r.guardrail_score for r in results) / total_cases,
            average_overall_score=sum(r.overall_score for r in results) / total_cases,
            pass_rate=passed_cases / total_cases,
        )
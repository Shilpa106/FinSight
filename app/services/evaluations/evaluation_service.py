from pathlib import Path
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.evaluation import Evaluation
from app.db.repositories.evaluation_repository import EvaluationRepository
from app.evals.dataset_loader import EvaluationDatasetLoader
from app.evals.evaluation_report import EvaluationReportGenerator
from app.evals.evaluation_runner import EvaluationRunner
from app.llm.llm_client import LLMClient
from app.rag.embeddings.embedding_client import EmbeddingClient
from app.rag.vectorstores.vectorstore_client import VectorStoreClient
from app.services.rag.rag_service import RAGService


class EvaluationService:
    def __init__(
        self,
        db: Session,
        embedding_client: EmbeddingClient,
        vectorstore_client: VectorStoreClient,
        llm_client: LLMClient,
    ) -> None:
        self.db = db
        self.repository = EvaluationRepository(db)
        self.dataset_loader = EvaluationDatasetLoader()
        self.report_generator = EvaluationReportGenerator()

        self.rag_service = RAGService(
            db=db,
            embedding_client=embedding_client,
            vectorstore_client=vectorstore_client,
            llm_client=llm_client,
        )

        self.runner = EvaluationRunner(
            rag_service=self.rag_service,
        )

    def run_evaluation(
        self,
        run_name: str,
        dataset_path: str,
    ) -> dict:
        dataset_name, cases = self.dataset_loader.load_dataset(dataset_path)

        results = []

        for case in cases:
            result = self.runner.run_case(case)
            results.append(result)

            evaluation = Evaluation(
                organization_id=case.organization_id,
                document_id=case.document_id,
                run_name=run_name,
                dataset_name=dataset_name,
                question=case.question,
                expected_answer=case.expected_answer,
                actual_answer=result.actual_answer,
                status="passed" if result.passed else "failed",
                retrieval_score=result.retrieval_score,
                answer_score=result.answer_score,
                citation_score=result.citation_score,
                guardrail_score=result.guardrail_score,
                overall_score=result.overall_score,
                metrics=result.metrics,
                result_metadata={
                    "case_id": result.case_id,
                    "citations": result.citations,
                    "retrieved_chunk_count": result.retrieved_chunk_count,
                    "guardrail_action": result.guardrail_action,
                    "passed": result.passed,
                },
                error_message=result.error_message,
            )

            self.repository.create(evaluation)

        summary = self.runner.summarize(
            run_name=run_name,
            dataset_name=dataset_name,
            results=results,
        )

        report = self.report_generator.generate_markdown_report(
            summary=summary,
            results=results,
        )

        self._write_report(
            run_name=run_name,
            report=report,
        )

        return {
            "summary": summary,
            "results": results,
            "report": report,
        }

    def list_evaluations_by_document(
        self,
        document_id: UUID,
        organization_id: UUID,
    ) -> list[Evaluation]:
        return self.repository.list_by_document(
            document_id=document_id,
            organization_id=organization_id,
        )

    def _write_report(
        self,
        run_name: str,
        report: str,
    ) -> None:
        reports_dir = Path("evals/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)

        safe_run_name = run_name.replace(" ", "_").lower()
        report_path = reports_dir / f"{safe_run_name}.md"

        with open(report_path, "w", encoding="utf-8") as file:
            file.write(report)
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.llm.llm_factory import get_llm_client
from app.rag.embeddings.embedding_factory import get_embedding_client
from app.rag.vectorstores.vectorstore_factory import get_vectorstore_client
from app.schemas.evaluation import (
    EvaluationListItemResponse,
    EvaluationRunRequest,
    EvaluationRunResponse,
)
from app.services.evaluations.evaluation_service import EvaluationService
from app.schemas.tasks import AsyncTaskResponse
from app.tasks.evaluation_tasks import run_evaluation_task

router = APIRouter()


@router.post("/run", response_model=EvaluationRunResponse)
def run_evaluation(
    request: EvaluationRunRequest,
    db: Session = Depends(get_db),
) -> EvaluationRunResponse:
    embedding_client = get_embedding_client()
    vectorstore_client = get_vectorstore_client()
    llm_client = get_llm_client()

    service = EvaluationService(
        db=db,
        embedding_client=embedding_client,
        vectorstore_client=vectorstore_client,
        llm_client=llm_client,
    )

    try:
        output = service.run_evaluation(
            run_name=request.run_name,
            dataset_path=request.dataset_path,
        )

        db.commit()

        summary = output["summary"]
        results = output["results"]

        return EvaluationRunResponse(
            run_name=summary.run_name,
            dataset_name=summary.dataset_name,
            total_cases=summary.total_cases,
            passed_cases=summary.passed_cases,
            failed_cases=summary.failed_cases,
            pass_rate=summary.pass_rate,
            average_retrieval_score=summary.average_retrieval_score,
            average_answer_score=summary.average_answer_score,
            average_citation_score=summary.average_citation_score,
            average_guardrail_score=summary.average_guardrail_score,
            average_overall_score=summary.average_overall_score,
            results=[
                {
                    "case_id": result.case_id,
                    "question": result.question,
                    "expected_answer": result.expected_answer,
                    "actual_answer": result.actual_answer,
                    "retrieval_score": result.retrieval_score,
                    "answer_score": result.answer_score,
                    "citation_score": result.citation_score,
                    "guardrail_score": result.guardrail_score,
                    "overall_score": result.overall_score,
                    "passed": result.passed,
                    "error_message": result.error_message,
                }
                for result in results
            ],
        )

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {str(error)}",
        ) from error


@router.get(
    "/documents/{document_id}",
    response_model=list[EvaluationListItemResponse],
)
def list_document_evaluations(
    document_id: UUID,
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> list[EvaluationListItemResponse]:
    embedding_client = get_embedding_client()
    vectorstore_client = get_vectorstore_client()
    llm_client = get_llm_client()

    service = EvaluationService(
        db=db,
        embedding_client=embedding_client,
        vectorstore_client=vectorstore_client,
        llm_client=llm_client,
    )

    evaluations = service.list_evaluations_by_document(
        document_id=document_id,
        organization_id=organization_id,
    )

    return evaluations

@router.post("/run/async", response_model=AsyncTaskResponse)
def run_evaluation_async(
    request: EvaluationRunRequest,
) -> AsyncTaskResponse:
    task = run_evaluation_task.delay(
        run_name=request.run_name,
        dataset_path=request.dataset_path,
    )

    return AsyncTaskResponse(
        task_id=task.id,
        workflow_run_id=None,
        document_id=None,
        status="queued",
        message="Evaluation task queued.",
    )

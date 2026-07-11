from uuid import UUID

from pydantic import BaseModel


class EvaluationRunRequest(BaseModel):
    run_name: str
    dataset_path: str


class EvaluationCaseResponse(BaseModel):
    case_id: str
    question: str
    expected_answer: str | None
    actual_answer: str | None
    retrieval_score: float
    answer_score: float
    citation_score: float
    guardrail_score: float
    overall_score: float
    passed: bool
    error_message: str | None = None


class EvaluationRunResponse(BaseModel):
    run_name: str
    dataset_name: str
    total_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float
    average_retrieval_score: float
    average_answer_score: float
    average_citation_score: float
    average_guardrail_score: float
    average_overall_score: float
    results: list[EvaluationCaseResponse]


class EvaluationListItemResponse(BaseModel):
    id: UUID
    run_name: str
    dataset_name: str
    question: str
    status: str
    retrieval_score: float | None
    answer_score: float | None
    citation_score: float | None
    guardrail_score: float | None
    overall_score: float | None

    class Config:
        from_attributes = True
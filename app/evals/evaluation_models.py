from uuid import UUID

from pydantic import BaseModel, Field


class EvaluationCase(BaseModel):
    case_id: str
    document_id: UUID
    organization_id: UUID
    user_id: UUID
    question: str
    expected_answer: str | None = None
    expected_keywords: list[str] = Field(default_factory=list)
    expected_pages: list[int] = Field(default_factory=list)
    should_trigger_guardrail: bool = False
    expected_guardrail_action: str | None = None


class EvaluationCaseResult(BaseModel):
    case_id: str
    question: str
    expected_answer: str | None
    actual_answer: str | None
    citations: list[dict]
    retrieved_chunk_count: int
    guardrail_action: str | None
    retrieval_score: float
    answer_score: float
    citation_score: float
    guardrail_score: float
    overall_score: float
    passed: bool
    metrics: dict
    error_message: str | None = None


class EvaluationRunSummary(BaseModel):
    run_name: str
    dataset_name: str
    total_cases: int
    passed_cases: int
    failed_cases: int
    average_retrieval_score: float
    average_answer_score: float
    average_citation_score: float
    average_guardrail_score: float
    average_overall_score: float
    pass_rate: float
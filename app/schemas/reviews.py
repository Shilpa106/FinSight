from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class HumanReviewResponse(BaseModel):
    id: UUID
    organization_id: UUID
    document_id: UUID
    session_id: UUID | None
    assistant_message_id: UUID | None
    workflow_run_id: UUID | None
    status: str
    reason: str
    question: str
    original_answer: str | None
    final_answer: str | None
    citations: list | None
    guardrail_metadata: dict | None
    review_metadata: dict | None
    reviewer_id: UUID | None
    reviewer_notes: str | None
    reviewed_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewListResponse(BaseModel):
    reviews: list[HumanReviewResponse]
    total: int


class ReviewDecisionRequest(BaseModel):
    reviewer_id: UUID
    reviewer_notes: str | None = None


class ReviewEditApproveRequest(BaseModel):
    reviewer_id: UUID
    final_answer: str = Field(min_length=1)
    reviewer_notes: str | None = None


class ReviewDecisionResponse(BaseModel):
    review_id: UUID
    status: str
    message: str
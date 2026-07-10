from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ChatQueryRequest(BaseModel):
    document_id: UUID
    organization_id: UUID
    user_id: UUID
    question: str = Field(min_length=3, max_length=2000)
    session_id: UUID | None = None


class CitationResponse(BaseModel):
    chunk_id: str
    document_id: str
    page_number: int | None
    chunk_index: int
    score: float | None
    preview: str


class ChatQueryResponse(BaseModel):
    session_id: UUID
    document_id: UUID
    question: str
    answer: str
    citations: list[CitationResponse]
    retrieved_chunk_count: int
    model_provider: str
    model_name: str


class ChatMessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    citations: list[dict] | None
    message_metadata: dict | None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    id: UUID
    organization_id: UUID
    user_id: UUID
    document_id: UUID
    title: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    session: ChatSessionResponse
    messages: list[ChatMessageResponse]
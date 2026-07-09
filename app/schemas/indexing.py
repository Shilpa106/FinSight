from uuid import UUID

from pydantic import BaseModel


class DocumentIndexingResponse(BaseModel):
    document_id: UUID
    status: str
    total_chunks: int
    message: str


class DocumentChunkResponse(BaseModel):
    id: UUID
    document_id: UUID
    chunk_index: int
    content: str
    page_number: int | None
    token_count: int | None
    vector_id: str | None
    chunk_metadata: dict | None

    class Config:
        from_attributes = True


class DocumentChunkListResponse(BaseModel):
    document_id: UUID
    chunks: list[DocumentChunkResponse]
    total: int
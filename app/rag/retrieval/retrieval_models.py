from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    chunk_id: str
    document_id: str
    organization_id: str
    chunk_index: int
    content: str
    page_number: int | None = None
    token_count: int | None = None
    score: float | None = None


class RetrievalResult(BaseModel):
    chunks: list[RetrievedChunk]
    total: int
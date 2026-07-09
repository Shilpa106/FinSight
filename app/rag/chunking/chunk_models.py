from pydantic import BaseModel


class TextChunk(BaseModel):
    chunk_index: int
    content: str
    page_number: int | None = None
    token_count: int
    metadata: dict | None = None


class ChunkingResult(BaseModel):
    chunks: list[TextChunk]
    total_chunks: int
    total_tokens: int
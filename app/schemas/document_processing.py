from uuid import UUID

from pydantic import BaseModel


class PageText(BaseModel):
    page_number: int
    text: str
    character_count: int


class TextExtractionResult(BaseModel):
    document_id: UUID
    full_text: str
    pages: list[PageText]
    page_count: int
    character_count: int
    extraction_metadata: dict | None = None


class DocumentProcessingResponse(BaseModel):
    document_id: UUID
    status: str
    message: str


class DocumentTextResponse(BaseModel):
    document_id: UUID
    page_count: int
    character_count: int
    full_text: str
    extraction_metadata: dict | None = None
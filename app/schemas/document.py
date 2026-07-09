from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    organization_id: UUID
    uploaded_by: UUID
    file_name: str
    file_type: str
    file_size_bytes: int
    storage_key: str
    checksum: str | None
    document_type: str
    status: str
    failure_reason: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentUploadResponse(BaseModel):
    document_id: UUID
    file_name: str
    file_type: str
    file_size_bytes: int
    status: str
    message: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int


class DocumentStatusResponse(BaseModel):
    document_id: UUID
    status: str
    failure_reason: str | None
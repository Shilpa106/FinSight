from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document_text import DocumentText
from app.integrations.storage.storage_client import StorageClient
from app.services.documents.document_processing_service import (
    DocumentProcessingService,
)

"""
Introduced a workflow boundary early, even before LangGraph, so later I can replace the internal implementation with LangGraph without changing the API layer.
"""
class DocumentProcessingWorkflow:
    def __init__(
        self,
        db: Session,
        storage_client: StorageClient,
    ) -> None:
        self.processing_service = DocumentProcessingService(
            db=db,
            storage_client=storage_client,
        )

    def run_text_extraction(
        self,
        document_id: UUID,
        organization_id: UUID,
        user_id: UUID | None = None,
    ) -> DocumentText:
        return self.processing_service.process_document_text_extraction(
            document_id=document_id,
            organization_id=organization_id,
            user_id=user_id,
        )
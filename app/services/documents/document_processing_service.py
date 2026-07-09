from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document_text import DocumentText
from app.db.models.workflow_run import WorkflowRun
from app.db.models.workflow_step import WorkflowStep
from app.db.repositories.document_repository import DocumentRepository
from app.db.repositories.document_text_repository import DocumentTextRepository
from app.db.repositories.workflow_repository import (
    WorkflowRunRepository,
    WorkflowStepRepository,
)
from app.enums.document_status import DocumentStatus
from app.enums.workflow_status import WorkflowStatus
from app.integrations.storage.storage_client import StorageClient
from app.services.audit.audit_service import AuditService
from app.services.ingestion.text_extraction_service import TextExtractionService


class DocumentProcessingService:
    def __init__(
        self,
        db: Session,
        storage_client: StorageClient,
    ) -> None:
        self.db = db
        self.storage_client = storage_client
        self.document_repository = DocumentRepository(db)
        self.document_text_repository = DocumentTextRepository(db)
        self.workflow_run_repository = WorkflowRunRepository(db)
        self.workflow_step_repository = WorkflowStepRepository(db)
        self.text_extraction_service = TextExtractionService()
        self.audit_service = AuditService(db)

    def process_document_text_extraction(
        self,
        document_id: UUID,
        organization_id: UUID,
        user_id: UUID | None = None,
    ) -> DocumentText:
        document = self.document_repository.get_by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        if document.organization_id != organization_id:
            raise PermissionError("Access denied.")

        workflow_run = self._create_workflow_run(
            organization_id=organization_id,
            document_id=document_id,
        )

        try:
            self._mark_workflow_running(workflow_run)

            self.document_repository.update_status(
                document_id=document_id,
                status=DocumentStatus.PROCESSING.value,
            )

            download_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="download_document",
                step_order=1,
            )

            content = self._run_step(
                step=download_step,
                fn=lambda: self.storage_client.download_file(document.storage_key),
            )

            extraction_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="extract_text",
                step_order=2,
            )

            extraction_result = self._run_step(
                step=extraction_step,
                fn=lambda: self.text_extraction_service.extract_text(
                    document_id=document.id,
                    file_type=document.file_type,
                    content=content,
                ),
            )

            persistence_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="persist_extracted_text",
                step_order=3,
            )

            document_text = self._run_step(
                step=persistence_step,
                fn=lambda: self.document_text_repository.upsert_document_text(
                    document_id=document.id,
                    organization_id=document.organization_id,
                    full_text=extraction_result.full_text,
                    page_count=extraction_result.page_count,
                    character_count=extraction_result.character_count,
                    extraction_metadata=extraction_result.extraction_metadata,
                ),
            )

            self.document_repository.update_status(
                document_id=document_id,
                status=DocumentStatus.TEXT_EXTRACTED.value,
            )

            self.audit_service.log_event(
                organization_id=organization_id,
                user_id=user_id,
                action="document.text_extracted",
                resource_type="document",
                resource_id=str(document_id),
                metadata={
                    "page_count": document_text.page_count,
                    "character_count": document_text.character_count,
                    "workflow_run_id": str(workflow_run.id),
                },
            )

            workflow_run.status = WorkflowStatus.COMPLETED.value
            workflow_run.completed_at = datetime.utcnow()

            return document_text

        except Exception as error:
            self.document_repository.update_status(
                document_id=document_id,
                status=DocumentStatus.FAILED.value,
                failure_reason=str(error),
            )

            workflow_run.status = WorkflowStatus.FAILED.value
            workflow_run.error_message = str(error)
            workflow_run.completed_at = datetime.utcnow()

            self.audit_service.log_event(
                organization_id=organization_id,
                user_id=user_id,
                action="document.text_extraction_failed",
                resource_type="document",
                resource_id=str(document_id),
                metadata={
                    "error": str(error),
                    "workflow_run_id": str(workflow_run.id),
                },
            )

            raise

    def get_document_text(
        self,
        document_id: UUID,
        organization_id: UUID,
    ) -> DocumentText:
        document = self.document_repository.get_by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        if document.organization_id != organization_id:
            raise PermissionError("Access denied.")

        document_text = self.document_text_repository.get_by_document_id(document_id)

        if document_text is None:
            raise ValueError("Extracted text not found.")

        return document_text

    def _create_workflow_run(
        self,
        organization_id: UUID,
        document_id: UUID,
    ) -> WorkflowRun:
        workflow_run = WorkflowRun(
            organization_id=organization_id,
            document_id=document_id,
            workflow_name="document_text_extraction",
            status=WorkflowStatus.PENDING.value,
        )

        return self.workflow_run_repository.create(workflow_run)

    def _mark_workflow_running(self, workflow_run: WorkflowRun) -> None:
        workflow_run.status = WorkflowStatus.RUNNING.value
        workflow_run.started_at = datetime.utcnow()
        self.db.flush()

    def _create_workflow_step(
        self,
        workflow_run_id: UUID,
        step_name: str,
        step_order: int,
    ) -> WorkflowStep:
        workflow_step = WorkflowStep(
            workflow_run_id=workflow_run_id,
            step_name=step_name,
            step_order=step_order,
            status=WorkflowStatus.PENDING.value,
        )

        return self.workflow_step_repository.create(workflow_step)

    def _run_step(self, step: WorkflowStep, fn):
        try:
            step.status = WorkflowStatus.RUNNING.value
            step.started_at = datetime.utcnow()
            self.db.flush()

            result = fn()

            step.status = WorkflowStatus.COMPLETED.value
            step.completed_at = datetime.utcnow()
            self.db.flush()

            return result

        except Exception as error:
            step.status = WorkflowStatus.FAILED.value
            step.error_message = str(error)
            step.completed_at = datetime.utcnow()
            self.db.flush()
            raise
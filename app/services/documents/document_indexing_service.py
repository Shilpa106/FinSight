from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document_chunk import DocumentChunk
from app.db.repositories.document_chunk_repository import DocumentChunkRepository
from app.db.repositories.document_repository import DocumentRepository
from app.db.repositories.document_text_repository import DocumentTextRepository
from app.db.repositories.workflow_repository import (
    WorkflowRunRepository,
    WorkflowStepRepository,
)
from app.enums.document_status import DocumentStatus
from app.enums.workflow_status import WorkflowStatus
from app.rag.embeddings.embedding_client import EmbeddingClient
from app.rag.vectorstores.vectorstore_client import VectorStoreClient
from app.services.audit.audit_service import AuditService
from app.services.ingestion.chunking_service import ChunkingService
from app.services.ingestion.embedding_service import EmbeddingService
from app.services.ingestion.indexing_service import IndexingService


class DocumentIndexingService:
    def __init__(
        self,
        db: Session,
        embedding_client: EmbeddingClient,
        vectorstore_client: VectorStoreClient,
    ) -> None:
        self.db = db

        self.document_repository = DocumentRepository(db)
        self.document_text_repository = DocumentTextRepository(db)
        self.document_chunk_repository = DocumentChunkRepository(db)
        self.workflow_run_repository = WorkflowRunRepository(db)
        self.workflow_step_repository = WorkflowStepRepository(db)

        self.chunking_service = ChunkingService()
        self.embedding_service = EmbeddingService(embedding_client)
        self.indexing_service = IndexingService(
            embedding_service=self.embedding_service,
            vectorstore_client=vectorstore_client,
        )

        self.vectorstore_client = vectorstore_client
        self.audit_service = AuditService(db)

    def index_document(
        self,
        document_id: UUID,
        organization_id: UUID,
        user_id: UUID | None = None,
    ) -> list[DocumentChunk]:
        document = self.document_repository.get_by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        if document.organization_id != organization_id:
            raise PermissionError("Access denied.")

        if document.status not in [
            DocumentStatus.TEXT_EXTRACTED.value,
            DocumentStatus.CHUNKED.value,
            DocumentStatus.EMBEDDED.value,
            DocumentStatus.INDEXED.value,
        ]:
            raise ValueError(
                f"Document must be text_extracted before indexing. "
                f"Current status: {document.status}"
            )

        document_text = self.document_text_repository.get_by_document_id(document_id)

        if document_text is None:
            raise ValueError("Extracted text not found.")

        workflow_run = self._create_workflow_run(
            organization_id=organization_id,
            document_id=document_id,
        )

        try:
            self._mark_workflow_running(workflow_run)

            # Step 1: chunk text
            chunk_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="chunk_document_text",
                step_order=1,
            )

            chunking_result = self._run_step(
                step=chunk_step,
                fn=lambda: self.chunking_service.chunk_text(document_text.full_text),
            )

            if not chunking_result.chunks:
                raise ValueError("No chunks were generated from document text.")

            # Remove old chunks and vectors for idempotency
            cleanup_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="cleanup_existing_chunks_and_vectors",
                step_order=2,
            )

            self._run_step(
                step=cleanup_step,
                fn=lambda: self._cleanup_existing_chunks_and_vectors(document_id),
            )

            # Step 3: persist chunks
            persist_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="persist_document_chunks",
                step_order=3,
            )

            created_chunks = self._run_step(
                step=persist_step,
                fn=lambda: self._persist_chunks(
                    document_id=document_id,
                    organization_id=organization_id,
                    chunks=chunking_result.chunks,
                ),
            )

            self.document_repository.update_status(
                document_id=document_id,
                status=DocumentStatus.CHUNKED.value,
            )

            # Step 4: generate embeddings and index vectors
            index_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="generate_embeddings_and_index_vectors",
                step_order=4,
            )

            indexed_chunks = self._run_step(
                step=index_step,
                fn=lambda: self.indexing_service.index_chunks(created_chunks),
            )

            self.document_repository.update_status(
                document_id=document_id,
                status=DocumentStatus.EMBEDDED.value,
            )

            # Step 5: persist vector IDs
            vector_id_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="persist_vector_ids",
                step_order=5,
            )

            self._run_step(
                step=vector_id_step,
                fn=lambda: self._persist_vector_ids(indexed_chunks),
            )

            self.document_repository.update_status(
                document_id=document_id,
                status=DocumentStatus.INDEXED.value,
            )

            workflow_run.status = WorkflowStatus.COMPLETED.value
            workflow_run.completed_at = datetime.utcnow()

            self.audit_service.log_event(
                organization_id=organization_id,
                user_id=user_id,
                action="document.indexed",
                resource_type="document",
                resource_id=str(document_id),
                metadata={
                    "workflow_run_id": str(workflow_run.id),
                    "total_chunks": len(created_chunks),
                    "total_tokens": chunking_result.total_tokens,
                },
            )

            return created_chunks

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
                action="document.indexing_failed",
                resource_type="document",
                resource_id=str(document_id),
                metadata={
                    "workflow_run_id": str(workflow_run.id),
                    "error": str(error),
                },
            )

            raise

    def list_document_chunks(
        self,
        document_id: UUID,
        organization_id: UUID,
    ) -> list[DocumentChunk]:
        document = self.document_repository.get_by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        if document.organization_id != organization_id:
            raise PermissionError("Access denied.")

        return self.document_chunk_repository.list_by_document(document_id)

    def _cleanup_existing_chunks_and_vectors(self, document_id: UUID) -> None:
        self.vectorstore_client.delete_by_document_id(str(document_id))
        self.document_chunk_repository.delete_by_document(document_id)

    def _persist_chunks(
        self,
        document_id: UUID,
        organization_id: UUID,
        chunks,
    ) -> list[DocumentChunk]:
        document_chunks: list[DocumentChunk] = []

        for chunk in chunks:
            document_chunks.append(
                DocumentChunk(
                    document_id=document_id,
                    organization_id=organization_id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    page_number=chunk.page_number,
                    token_count=chunk.token_count,
                    chunk_metadata=chunk.metadata,
                )
            )

        return self.document_chunk_repository.bulk_create(document_chunks)

    def _persist_vector_ids(
        self,
        indexed_chunks: list[tuple[DocumentChunk, str]],
    ) -> None:
        for chunk, vector_id in indexed_chunks:
            self.document_chunk_repository.update_vector_id(
                chunk_id=chunk.id,
                vector_id=vector_id,
            )

    def _create_workflow_run(
        self,
        organization_id: UUID,
        document_id: UUID,
    ):
        from app.db.models.workflow_run import WorkflowRun

        workflow_run = WorkflowRun(
            organization_id=organization_id,
            document_id=document_id,
            workflow_name="document_indexing",
            status=WorkflowStatus.PENDING.value,
        )

        return self.workflow_run_repository.create(workflow_run)

    def _mark_workflow_running(self, workflow_run) -> None:
        workflow_run.status = WorkflowStatus.RUNNING.value
        workflow_run.started_at = datetime.utcnow()
        self.db.flush()

    def _create_workflow_step(
        self,
        workflow_run_id: UUID,
        step_name: str,
        step_order: int,
    ):
        from app.db.models.workflow_step import WorkflowStep

        workflow_step = WorkflowStep(
            workflow_run_id=workflow_run_id,
            step_name=step_name,
            step_order=step_order,
            status=WorkflowStatus.PENDING.value,
        )

        return self.workflow_step_repository.create(workflow_step)

    def _run_step(self, step, fn):
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
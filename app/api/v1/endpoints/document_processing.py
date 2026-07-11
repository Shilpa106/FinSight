from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.integrations.storage.storage_factory import get_storage_client
from app.schemas.document_processing import (
    DocumentProcessingResponse,
    DocumentTextResponse,
)
from app.services.documents.document_processing_service import (
    DocumentProcessingService,
)
from app.schemas.tasks import AsyncTaskResponse
from app.tasks.document_tasks import extract_document_text_task
from app.tasks.pipeline_tasks import document_full_pipeline_task

router = APIRouter()



@router.post("/{document_id}/process-text", response_model=DocumentProcessingResponse)
def process_document_text(
    document_id: UUID,
    organization_id: UUID,
    user_id: UUID | None = None,
    db: Session = Depends(get_db),
) -> DocumentProcessingResponse:
    storage_client = get_storage_client()
    processing_service = DocumentProcessingService(
        db=db,
        storage_client=storage_client,
    )

    try:
        document_text = processing_service.process_document_text_extraction(
            document_id=document_id,
            organization_id=organization_id,
            user_id=user_id,
        )

        db.commit()

        return DocumentProcessingResponse(
            document_id=document_id,
            status="text_extracted",
            message=(
                f"Text extracted successfully. "
                f"Pages: {document_text.page_count}, "
                f"Characters: {document_text.character_count}"
            ),
        )

    except PermissionError as error:
        db.rollback()
        raise HTTPException(status_code=403, detail=str(error)) from error

    except ValueError as error:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(error)) from error

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Document text extraction failed: {str(error)}",
        ) from error


@router.get("/{document_id}/text", response_model=DocumentTextResponse)
def get_document_text(
    document_id: UUID,
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> DocumentTextResponse:
    storage_client = get_storage_client()
    processing_service = DocumentProcessingService(
        db=db,
        storage_client=storage_client,
    )

    try:
        document_text = processing_service.get_document_text(
            document_id=document_id,
            organization_id=organization_id,
        )

        return DocumentTextResponse(
            document_id=document_text.document_id,
            page_count=document_text.page_count,
            character_count=document_text.character_count,
            full_text=document_text.full_text,
            extraction_metadata=document_text.extraction_metadata,
        )

    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    

@router.post("/{document_id}/process-text/async", response_model=AsyncTaskResponse)
def process_document_text_async(
    document_id: UUID,
    organization_id: UUID,
    user_id: UUID | None = None,
) -> AsyncTaskResponse:
    task = extract_document_text_task.delay(
        document_id=str(document_id),
        organization_id=str(organization_id),
        user_id=str(user_id) if user_id else None,
    )

    return AsyncTaskResponse(
        task_id=task.id,
        workflow_run_id=None,
        document_id=document_id,
        status="queued",
        message="Document text extraction task queued.",
    )


@router.post("/{document_id}/pipeline/async", response_model=AsyncTaskResponse)
def process_document_pipeline_async(
    document_id: UUID,
    organization_id: UUID,
    user_id: UUID | None = None,
) -> AsyncTaskResponse:
    task = document_full_pipeline_task.delay(
        document_id=str(document_id),
        organization_id=str(organization_id),
        user_id=str(user_id) if user_id else None,
    )

    return AsyncTaskResponse(
        task_id=task.id,
        workflow_run_id=None,
        document_id=document_id,
        status="queued",
        message="Document processing pipeline task queued.",
    )
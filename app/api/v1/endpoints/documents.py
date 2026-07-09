from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.integrations.storage.storage_factory import get_storage_client
from app.schemas.document import (
    DocumentListResponse,
    DocumentResponse,
    DocumentStatusResponse,
    DocumentUploadResponse,
)
from app.services.documents.document_access_service import DocumentAccessService
from app.services.documents.document_service import DocumentService
from app.services.documents.upload_service import UploadService
from app.services.ingestion.file_validation_service import FileValidationError

router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    request: Request,
    organization_id: UUID,
    user_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> DocumentUploadResponse:
    storage_client = get_storage_client()
    upload_service = UploadService(db=db, storage_client=storage_client)

    try:
        document = await upload_service.upload_document(
            organization_id=organization_id,
            user_id=user_id,
            file=file,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        db.commit()

        return DocumentUploadResponse(
            document_id=document.id,
            file_name=document.file_name,
            file_type=document.file_type,
            file_size_bytes=document.file_size_bytes,
            status=document.status,
            message="Document uploaded successfully.",
        )

    except FileValidationError as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error)) from error

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to upload document.",
        ) from error


@router.get("", response_model=DocumentListResponse)
def list_documents(
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> DocumentListResponse:
    document_service = DocumentService(db)
    documents = document_service.list_documents(organization_id=organization_id)

    return DocumentListResponse(
        documents=documents,
        total=len(documents),
    )


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: UUID,
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> DocumentResponse:
    document_service = DocumentService(db)
    access_service = DocumentAccessService()

    document = document_service.get_document(document_id=document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    if not access_service.can_access_document(
        document=document,
        organization_id=organization_id,
    ):
        raise HTTPException(status_code=403, detail="Access denied.")

    return document


@router.get("/{document_id}/status", response_model=DocumentStatusResponse)
def get_document_status(
    document_id: UUID,
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> DocumentStatusResponse:
    document_service = DocumentService(db)
    access_service = DocumentAccessService()

    document = document_service.get_document(document_id=document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    if not access_service.can_access_document(
        document=document,
        organization_id=organization_id,
    ):
        raise HTTPException(status_code=403, detail="Access denied.")

    return DocumentStatusResponse(
        document_id=document.id,
        status=document.status,
        failure_reason=document.failure_reason,
    )
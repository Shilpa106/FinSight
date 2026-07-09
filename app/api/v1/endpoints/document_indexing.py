from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.rag.embeddings.embedding_factory import get_embedding_client
from app.rag.vectorstores.vectorstore_factory import get_vectorstore_client
from app.schemas.indexing import (
    DocumentChunkListResponse,
    DocumentIndexingResponse,
)
from app.services.documents.document_indexing_service import DocumentIndexingService

router = APIRouter()


@router.post("/{document_id}/index", response_model=DocumentIndexingResponse)
def index_document(
    document_id: UUID,
    organization_id: UUID,
    user_id: UUID | None = None,
    db: Session = Depends(get_db),
) -> DocumentIndexingResponse:
    embedding_client = get_embedding_client()
    vectorstore_client = get_vectorstore_client()

    indexing_service = DocumentIndexingService(
        db=db,
        embedding_client=embedding_client,
        vectorstore_client=vectorstore_client,
    )

    try:
        chunks = indexing_service.index_document(
            document_id=document_id,
            organization_id=organization_id,
            user_id=user_id,
        )

        db.commit()

        return DocumentIndexingResponse(
            document_id=document_id,
            status="indexed",
            total_chunks=len(chunks),
            message="Document indexed successfully.",
        )

    except PermissionError as error:
        db.rollback()
        raise HTTPException(status_code=403, detail=str(error)) from error

    except ValueError as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error)) from error

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Document indexing failed: {str(error)}",
        ) from error


@router.get("/{document_id}/chunks", response_model=DocumentChunkListResponse)
def list_document_chunks(
    document_id: UUID,
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> DocumentChunkListResponse:
    embedding_client = get_embedding_client()
    vectorstore_client = get_vectorstore_client()

    indexing_service = DocumentIndexingService(
        db=db,
        embedding_client=embedding_client,
        vectorstore_client=vectorstore_client,
    )

    try:
        chunks = indexing_service.list_document_chunks(
            document_id=document_id,
            organization_id=organization_id,
        )

        return DocumentChunkListResponse(
            document_id=document_id,
            chunks=chunks,
            total=len(chunks),
        )

    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
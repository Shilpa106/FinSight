from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.llm.llm_factory import get_llm_client
from app.rag.embeddings.embedding_factory import get_embedding_client
from app.rag.vectorstores.vectorstore_factory import get_vectorstore_client
from app.schemas.chat import (
    ChatHistoryResponse,
    ChatQueryRequest,
    ChatQueryResponse,
)
from app.services.chat.chat_service import ChatService
from app.services.rag.rag_service import RAGService

router = APIRouter()


@router.post("/query", response_model=ChatQueryResponse)
def query_document(
    request: ChatQueryRequest,
    db: Session = Depends(get_db),
) -> ChatQueryResponse:
    embedding_client = get_embedding_client()
    vectorstore_client = get_vectorstore_client()
    llm_client = get_llm_client()

    rag_service = RAGService(
        db=db,
        embedding_client=embedding_client,
        vectorstore_client=vectorstore_client,
        llm_client=llm_client,
    )

    try:
        result = rag_service.answer_question(
            organization_id=request.organization_id,
            user_id=request.user_id,
            document_id=request.document_id,
            question=request.question,
            session_id=request.session_id,
        )

        db.commit()

        return result

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
            detail=f"RAG query failed: {str(error)}",
        ) from error


@router.get("/sessions/{session_id}", response_model=ChatHistoryResponse)
def get_chat_history(
    session_id: UUID,
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> ChatHistoryResponse:
    chat_service = ChatService(db)

    try:
        session, messages = chat_service.get_chat_history(
            session_id=session_id,
            organization_id=organization_id,
        )

        return ChatHistoryResponse(
            session=session,
            messages=messages,
        )

    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.chat_message import ChatMessage
from app.db.models.chat_session import ChatSession
from app.db.repositories.chat_repository import (
    ChatMessageRepository,
    ChatSessionRepository,
)


class ChatService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.session_repository = ChatSessionRepository(db)
        self.message_repository = ChatMessageRepository(db)

    def get_or_create_session(
        self,
        organization_id: UUID,
        user_id: UUID,
        document_id: UUID,
        session_id: UUID | None = None,
        title: str | None = None,
    ) -> ChatSession:
        if session_id is not None:
            existing_session = self.session_repository.get_by_id(session_id)

            if existing_session is None:
                raise ValueError("Chat session not found.")

            if existing_session.organization_id != organization_id:
                raise PermissionError("Access denied.")

            return existing_session

        session = ChatSession(
            organization_id=organization_id,
            user_id=user_id,
            document_id=document_id,
            title=title,
        )

        return self.session_repository.create(session)

    def add_message(
        self,
        session_id: UUID,
        role: str,
        content: str,
        citations: list[dict] | None = None,
        metadata: dict | None = None,
    ) -> ChatMessage:
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            citations=citations,
            message_metadata=metadata,
        )

        return self.message_repository.create(message)

    def get_chat_history(
        self,
        session_id: UUID,
        organization_id: UUID,
    ) -> tuple[ChatSession, list[ChatMessage]]:
        session = self.session_repository.get_by_id(session_id)

        if session is None:
            raise ValueError("Chat session not found.")

        if session.organization_id != organization_id:
            raise PermissionError("Access denied.")

        messages = self.message_repository.list_by_session(session_id)

        return session, messages
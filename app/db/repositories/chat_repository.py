from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.chat_message import ChatMessage
from app.db.models.chat_session import ChatSession
from app.db.repositories.base_repository import BaseRepository


class ChatSessionRepository(BaseRepository[ChatSession]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, ChatSession)

    def get_by_id(self, session_id: UUID) -> ChatSession | None:
        return (
            self.db.query(ChatSession)
            .filter(ChatSession.id == session_id)
            .first()
        )

    def list_by_document(
        self,
        document_id: UUID,
        organization_id: UUID,
    ) -> list[ChatSession]:
        return (
            self.db.query(ChatSession)
            .filter(
                ChatSession.document_id == document_id,
                ChatSession.organization_id == organization_id,
            )
            .order_by(ChatSession.created_at.desc())
            .all()
        )


class ChatMessageRepository(BaseRepository[ChatMessage]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, ChatMessage)

    def list_by_session(self, session_id: UUID) -> list[ChatMessage]:
        return (
            self.db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )
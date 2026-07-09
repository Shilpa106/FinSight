from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.audit_log import AuditLog
from app.db.repositories.base_repository import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, AuditLog)

    def list_by_organization(self, organization_id: UUID, limit: int = 100) -> list[AuditLog]:
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.organization_id == organization_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .all()
        )
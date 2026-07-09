from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.audit_log import AuditLog
from app.db.repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.audit_repository = AuditRepository(db)

    def log_event(
        self,
        organization_id: UUID,
        action: str,
        resource_type: str,
        resource_id: str | None = None,
        user_id: UUID | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        audit_log = AuditLog(
            organization_id=organization_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            audit_metadata=metadata,
        )

        return self.audit_repository.create(audit_log)
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, User)

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def list_by_organization(self, organization_id: UUID) -> list[User]:
        return (
            self.db.query(User)
            .filter(User.organization_id == organization_id)
            .order_by(User.created_at.desc())
            .all()
        )
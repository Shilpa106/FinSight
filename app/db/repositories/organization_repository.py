from sqlalchemy.orm import Session

from app.db.models.organization import Organization
from app.db.repositories.base_repository import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Organization)

    def get_by_slug(self, slug: str) -> Organization | None:
        return self.db.query(Organization).filter(Organization.slug == slug).first()
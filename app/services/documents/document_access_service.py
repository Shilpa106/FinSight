from uuid import UUID

from app.db.models.document import Document

"""
I introduced document access checks early so tenant isolation becomes part of the architecture instead of an afterthought.

"""
class DocumentAccessService:
    def can_access_document(
        self,
        document: Document,
        organization_id: UUID,
    ) -> bool:
        return document.organization_id == organization_id
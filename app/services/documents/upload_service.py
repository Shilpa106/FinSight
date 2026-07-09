import uuid
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.db.models.document import Document
from app.db.repositories.document_repository import DocumentRepository
from app.enums.document_status import DocumentStatus
from app.enums.document_type import DocumentType
from app.integrations.storage.storage_client import StorageClient
from app.services.audit.audit_service import AuditService
from app.services.ingestion.checksum_service import ChecksumService
from app.services.ingestion.file_validation_service import FileValidationService
from app.utils.file_utils import build_storage_key, get_file_extension


class UploadService:
    def __init__(
        self,
        db: Session,
        storage_client: StorageClient,
    ) -> None:
        self.db = db
        self.storage_client = storage_client
        self.document_repository = DocumentRepository(db)
        self.file_validation_service = FileValidationService()
        self.checksum_service = ChecksumService()
        self.audit_service = AuditService(db)

    async def upload_document(
        self,
        organization_id: UUID,
        user_id: UUID,
        file: UploadFile,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> Document:
        content = await self.file_validation_service.validate(file)

        checksum = self.checksum_service.generate_sha256(content)
        document_id = uuid.uuid4()

        file_name = file.filename or "uploaded_file"
        file_type = get_file_extension(file_name)
        content_type = file.content_type or "application/octet-stream"

        storage_key = build_storage_key(
            organization_id=str(organization_id),
            document_id=str(document_id),
            filename=file_name,
        )

        self.storage_client.upload_file(
            storage_key=storage_key,
            content=content,
            content_type=content_type,
        )

        document = Document(
            id=document_id,
            organization_id=organization_id,
            uploaded_by=user_id,
            file_name=file_name,
            file_type=file_type,
            file_size_bytes=len(content),
            storage_key=storage_key,
            checksum=checksum,
            document_type=DocumentType.UNKNOWN.value,
            status=DocumentStatus.UPLOADED.value,
        )

        created_document = self.document_repository.create(document)

        self.audit_service.log_event(
            organization_id=organization_id,
            user_id=user_id,
            action="document.uploaded",
            resource_type="document",
            resource_id=str(created_document.id),
            ip_address=ip_address,
            user_agent=user_agent,
            metadata={
                "file_name": file_name,
                "file_type": file_type,
                "file_size_bytes": len(content),
                "storage_key": storage_key,
                "checksum": checksum,
            },
        )

        return created_document
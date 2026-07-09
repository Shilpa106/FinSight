from app.core.config import settings
from app.integrations.storage.local_storage_client import LocalStorageClient
from app.integrations.storage.s3_client import S3StorageClient
from app.integrations.storage.storage_client import StorageClient


def get_storage_client() -> StorageClient:
    if settings.STORAGE_PROVIDER == "local":
        return LocalStorageClient(base_path=settings.LOCAL_STORAGE_PATH)

    if settings.STORAGE_PROVIDER == "s3":
        return S3StorageClient(
            bucket_name=settings.S3_BUCKET_NAME,
            region_name=settings.S3_REGION,
            access_key_id=settings.AWS_ACCESS_KEY_ID,
            secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.S3_ENDPOINT_URL,
        )

    raise ValueError(f"Unsupported storage provider: {settings.STORAGE_PROVIDER}")
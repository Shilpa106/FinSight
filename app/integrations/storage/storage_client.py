from abc import ABC, abstractmethod

"""
Storage interface so local development can use filesystem storage while production can use S3 or MinIO without changing business logic.

"""

class StorageClient(ABC):
    @abstractmethod
    def upload_file(
        self,
        storage_key: str,
        content: bytes,
        content_type: str,
    ) -> str:
        pass

    @abstractmethod
    def download_file(self, storage_key: str) -> bytes:
        pass

    @abstractmethod
    def delete_file(self, storage_key: str) -> None:
        pass

    @abstractmethod
    def file_exists(self, storage_key: str) -> bool:
        pass
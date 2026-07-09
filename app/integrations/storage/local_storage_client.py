from pathlib import Path

from app.integrations.storage.storage_client import StorageClient


class LocalStorageClient(StorageClient):
    def __init__(self, base_path: str) -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def upload_file(
        self,
        storage_key: str,
        content: bytes,
        content_type: str,
    ) -> str:
        file_path = self.base_path / storage_key
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "wb") as file:
            file.write(content)

        return storage_key

    def download_file(self, storage_key: str) -> bytes:
        file_path = self.base_path / storage_key

        with open(file_path, "rb") as file:
            return file.read()

    def delete_file(self, storage_key: str) -> None:
        file_path = self.base_path / storage_key

        if file_path.exists():
            file_path.unlink()

    def file_exists(self, storage_key: str) -> bool:
        file_path = self.base_path / storage_key
        return file_path.exists()
import boto3

from app.integrations.storage.storage_client import StorageClient


class S3StorageClient(StorageClient):
    def __init__(
        self,
        bucket_name: str,
        region_name: str,
        access_key_id: str | None,
        secret_access_key: str | None,
        endpoint_url: str | None = None,
    ) -> None:
        self.bucket_name = bucket_name

        self.client = boto3.client(
            "s3",
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            endpoint_url=endpoint_url,
        )

        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        existing_buckets = self.client.list_buckets()
        bucket_names = [
            bucket["Name"]
            for bucket in existing_buckets.get("Buckets", [])
        ]

        if self.bucket_name not in bucket_names:
            self.client.create_bucket(Bucket=self.bucket_name)

    def upload_file(
        self,
        storage_key: str,
        content: bytes,
        content_type: str,
    ) -> str:
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=storage_key,
            Body=content,
            ContentType=content_type,
        )

        return storage_key

    def download_file(self, storage_key: str) -> bytes:
        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=storage_key,
        )

        return response["Body"].read()

    def delete_file(self, storage_key: str) -> None:
        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=storage_key,
        )

    def file_exists(self, storage_key: str) -> bool:
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=storage_key,
            )
            return True
        except Exception:
            return False
from app.integrations.storage.local_storage_client import LocalStorageClient


def test_local_storage_upload_and_download(tmp_path) -> None:
    client = LocalStorageClient(base_path=str(tmp_path))

    storage_key = "organizations/org-1/documents/doc-1/sample.txt"
    content = b"sample content"

    client.upload_file(
        storage_key=storage_key,
        content=content,
        content_type="text/plain",
    )

    assert client.file_exists(storage_key) is True
    assert client.download_file(storage_key) == content

    client.delete_file(storage_key)

    assert client.file_exists(storage_key) is False
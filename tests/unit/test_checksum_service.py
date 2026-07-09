from app.services.ingestion.checksum_service import ChecksumService


def test_generate_sha256_checksum() -> None:
    service = ChecksumService()

    checksum = service.generate_sha256(b"hello")

    assert checksum == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
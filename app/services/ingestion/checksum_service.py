import hashlib


class ChecksumService:
    def generate_sha256(self, content: bytes) -> str:
        sha256 = hashlib.sha256()
        sha256.update(content)
        return sha256.hexdigest()
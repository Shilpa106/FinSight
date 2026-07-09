from pathlib import Path


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower().replace(".", "")


def sanitize_filename(filename: str) -> str:
    allowed_chars = []

    for char in filename:
        if char.isalnum() or char in ["-", "_", ".", " "]:
            allowed_chars.append(char)
        else:
            allowed_chars.append("_")

    sanitized = "".join(allowed_chars).strip()

    if not sanitized:
        return "uploaded_file"

    return sanitized


def build_storage_key(
    organization_id: str,
    document_id: str,
    filename: str,
) -> str:
    sanitized_filename = sanitize_filename(filename)

    return f"organizations/{organization_id}/documents/{document_id}/{sanitized_filename}"
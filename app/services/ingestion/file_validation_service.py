from fastapi import UploadFile

from app.utils.file_utils import get_file_extension


class FileValidationError(Exception):
    pass


class FileValidationService:
    def __init__(self) -> None:
        self.allowed_extensions = {
            "pdf",
            "docx",
            "csv",
            "xlsx",
            "txt",
        }

        self.allowed_content_types = {
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "text/plain",
        }

        self.max_file_size_bytes = 25 * 1024 * 1024

    async def validate(self, file: UploadFile) -> bytes:
        if file.filename is None:
            raise FileValidationError("File name is required.")

        extension = get_file_extension(file.filename)

        if extension not in self.allowed_extensions:
            raise FileValidationError(
                f"Unsupported file type: {extension}. "
                f"Allowed types: {', '.join(sorted(self.allowed_extensions))}"
            )

        if file.content_type not in self.allowed_content_types:
            raise FileValidationError(
                f"Unsupported content type: {file.content_type}"
            )

        content = await file.read()

        if len(content) == 0:
            raise FileValidationError("Uploaded file is empty.")

        if len(content) > self.max_file_size_bytes:
            raise FileValidationError(
                f"File size exceeds limit of {self.max_file_size_bytes} bytes."
            )

        await file.seek(0)

        return content
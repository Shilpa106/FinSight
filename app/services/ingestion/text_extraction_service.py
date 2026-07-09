from uuid import UUID

from app.document_processing.loaders.pdf_loader import PDFLoader
from app.document_processing.preprocessors.text_cleaner import TextCleaner
from app.document_processing.validators.text_extraction_validator import (
    TextExtractionValidator,
)
from app.schemas.document_processing import PageText, TextExtractionResult


class UnsupportedDocumentTypeError(Exception):
    pass


class TextExtractionService:
    def __init__(self) -> None:
        self.pdf_loader = PDFLoader()
        self.text_cleaner = TextCleaner()
        self.validator = TextExtractionValidator()

    def extract_text(
        self,
        document_id: UUID,
        file_type: str,
        content: bytes,
    ) -> TextExtractionResult:
        if file_type != "pdf":
            raise UnsupportedDocumentTypeError(
                f"Text extraction is currently supported only for PDF files. "
                f"Received: {file_type}"
            )

        result = self.pdf_loader.extract_text(
            document_id=document_id,
            content=content,
        )

        cleaned_pages: list[PageText] = []
        cleaned_full_text_parts: list[str] = []

        for page in result.pages:
            cleaned_text = self.text_cleaner.clean(page.text)

            cleaned_pages.append(
                PageText(
                    page_number=page.page_number,
                    text=cleaned_text,
                    character_count=len(cleaned_text),
                )
            )

            if cleaned_text:
                cleaned_full_text_parts.append(
                    f"\n\n--- Page {page.page_number} ---\n\n{cleaned_text}"
                )

        cleaned_full_text = "".join(cleaned_full_text_parts).strip()

        cleaned_result = TextExtractionResult(
            document_id=document_id,
            full_text=cleaned_full_text,
            pages=cleaned_pages,
            page_count=result.page_count,
            character_count=len(cleaned_full_text),
            extraction_metadata={
                **(result.extraction_metadata or {}),
                "cleaner": "basic_text_cleaner",
            },
        )

        self.validator.validate(cleaned_result)

        return cleaned_result
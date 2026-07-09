from io import BytesIO
from uuid import UUID

from pypdf import PdfReader

from app.schemas.document_processing import PageText, TextExtractionResult


class PDFTextExtractionError(Exception):
    pass


class PDFLoader:
    def extract_text(
        self,
        document_id: UUID,
        content: bytes,
    ) -> TextExtractionResult:
        try:
            reader = PdfReader(BytesIO(content))
        except Exception as error:
            raise PDFTextExtractionError("Failed to read PDF file.") from error

        pages: list[PageText] = []
        full_text_parts: list[str] = []

        for index, page in enumerate(reader.pages):
            page_number = index + 1

            try:
                page_text = page.extract_text() or ""
            except Exception:
                page_text = ""

            page_text = page_text.strip()

            pages.append(
                PageText(
                    page_number=page_number,
                    text=page_text,
                    character_count=len(page_text),
                )
            )

            if page_text:
                full_text_parts.append(
                    f"\n\n--- Page {page_number} ---\n\n{page_text}"
                )

        full_text = "".join(full_text_parts).strip()

        return TextExtractionResult(
            document_id=document_id,
            full_text=full_text,
            pages=pages,
            page_count=len(pages),
            character_count=len(full_text),
            extraction_metadata={
                "loader": "pypdf",
                "page_count": len(pages),
                "empty_pages": len([page for page in pages if not page.text.strip()]),
            },
        )
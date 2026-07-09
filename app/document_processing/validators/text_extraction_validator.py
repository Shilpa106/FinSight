from app.schemas.document_processing import TextExtractionResult


class TextExtractionValidationError(Exception):
    pass


class TextExtractionValidator:
    def validate(self, result: TextExtractionResult) -> None:
        if result.page_count <= 0:
            raise TextExtractionValidationError("Document has no pages.")

        if not result.full_text.strip():
            raise TextExtractionValidationError(
                "No text could be extracted from document. "
                "The file may be scanned or image-based. OCR is not enabled yet."
            )

        if result.character_count < 20:
            raise TextExtractionValidationError(
                "Extracted text is too short to process."
            )
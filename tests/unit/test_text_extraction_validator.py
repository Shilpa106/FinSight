from uuid import uuid4

import pytest

from app.document_processing.validators.text_extraction_validator import (
    TextExtractionValidationError,
    TextExtractionValidator,
)
from app.schemas.document_processing import TextExtractionResult


def test_validator_rejects_empty_text() -> None:
    validator = TextExtractionValidator()

    result = TextExtractionResult(
        document_id=uuid4(),
        full_text="",
        pages=[],
        page_count=0,
        character_count=0,
        extraction_metadata=None,
    )

    with pytest.raises(TextExtractionValidationError):
        validator.validate(result)


def test_validator_accepts_valid_text() -> None:
    validator = TextExtractionValidator()

    result = TextExtractionResult(
        document_id=uuid4(),
        full_text="This is a valid financial document with enough text.",
        pages=[],
        page_count=1,
        character_count=52,
        extraction_metadata=None,
    )

    validator.validate(result)
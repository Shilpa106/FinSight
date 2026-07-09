from abc import ABC, abstractmethod

from app.schemas.document_processing import TextExtractionResult


class BaseDocumentLoader(ABC):
    @abstractmethod
    def extract_text(
        self,
        document_id: str,
        content: bytes,
    ) -> TextExtractionResult:
        pass
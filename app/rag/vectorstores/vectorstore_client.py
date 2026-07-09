from abc import ABC, abstractmethod


class VectorStoreClient(ABC):
    @abstractmethod
    def ensure_collection(self) -> None:
        pass

    @abstractmethod
    def upsert_vectors(
        self,
        vectors: list[dict],
    ) -> None:
        pass

    @abstractmethod
    def delete_by_document_id(
        self,
        document_id: str,
    ) -> None:
        pass
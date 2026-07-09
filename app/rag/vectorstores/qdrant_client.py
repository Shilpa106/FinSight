from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.rag.vectorstores.vectorstore_client import VectorStoreClient


class QdrantVectorStoreClient(VectorStoreClient):
    def __init__(
        self,
        url: str,
        collection_name: str,
        vector_size: int,
    ) -> None:
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size

    def ensure_collection(self) -> None:
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]

        if self.collection_name in collection_names:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert_vectors(
        self,
        vectors: list[dict],
    ) -> None:
        points: list[PointStruct] = []

        for vector in vectors:
            points.append(
                PointStruct(
                    id=vector["id"],
                    vector=vector["embedding"],
                    payload=vector["payload"],
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def delete_by_document_id(
        self,
        document_id: str,
    ) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
        )
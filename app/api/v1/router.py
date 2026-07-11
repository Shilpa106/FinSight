from fastapi import APIRouter

from app.api.v1.endpoints.chat import router as chat_router
from app.api.v1.endpoints.document_indexing import router as document_indexing_router
from app.api.v1.endpoints.document_processing import router as document_processing_router
from app.api.v1.endpoints.documents import router as documents_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.evaluations import router as evaluations_router
from app.api.v1.endpoints.reviews import router as reviews_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(documents_router, prefix="/documents", tags=["Documents"])
router.include_router(
    document_processing_router,
    prefix="/documents",
    tags=["Document Processing"],
)
router.include_router(
    document_indexing_router,
    prefix="/documents",
    tags=["Document Indexing"],
)
router.include_router(chat_router, prefix="/chat", tags=["Chat"])

router.include_router(
    evaluations_router,
    prefix="/evaluations",
    tags=["Evaluations"],
)

router.include_router(
    reviews_router,
    prefix="/reviews",
    tags=["Human Reviews"],
)
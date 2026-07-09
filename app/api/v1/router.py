from fastapi import APIRouter

from app.api.v1.endpoints.document_processing import router as document_processing_router
from app.api.v1.endpoints.documents import router as documents_router
from app.api.v1.endpoints.health import router as health_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(documents_router, prefix="/documents", tags=["Documents"])
router.include_router(
    document_processing_router,
    prefix="/documents",
    tags=["Document Processing"],
)
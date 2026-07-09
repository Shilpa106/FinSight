from fastapi import APIRouter

router = APIRouter()


@router.get("")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "finsight-api",
        "version": "0.1.0",
    }
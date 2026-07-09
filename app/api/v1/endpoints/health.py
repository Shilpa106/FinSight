from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get("")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "finsight-api",
        "version": "0.1.0",
    }


@router.get("/db")
def database_health_check(db: Session = Depends(get_db)) -> dict:
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
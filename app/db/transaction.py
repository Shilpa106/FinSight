from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


@contextmanager
def transactional_session() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
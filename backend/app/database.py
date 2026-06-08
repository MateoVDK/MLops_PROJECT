import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

log = logging.getLogger(__name__)


def _get_database_url():
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    # default to cluster service name; in local dev you can set DATABASE_URL
    return "postgresql://postgres:postgres@postgres-service:5432/postgres"


DATABASE_URL = _get_database_url()


engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create database tables for the models. Safe to call multiple times."""
    try:
        Base.metadata.create_all(bind=engine)
        log.info("Database tables created or already exist")
    except Exception:
        log.exception("Failed to create DB tables")
        raise


def get_db():
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    # quick command-line check
    print("DATABASE_URL:", DATABASE_URL)
    try:
        init_db()
        print("init_db succeeded")
    except Exception as e:
        print("init_db failed:", e)

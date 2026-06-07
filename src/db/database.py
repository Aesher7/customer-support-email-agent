"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.core.config import get_settings
from src.core.logger import setup_logger

logger = setup_logger(__name__)

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    from src.db.models import Base

    logger.info("Initializing database")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")

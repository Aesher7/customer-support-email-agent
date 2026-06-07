"""Base service class."""

from sqlalchemy.orm import Session
from src.core.logger import setup_logger


class BaseService:
    """Base service with common functionality."""

    def __init__(self, db: Session = None):
        """Initialize service."""
        self.db = db
        self.logger = setup_logger(self.__class__.__name__)

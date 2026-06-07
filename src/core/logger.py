"""Logging configuration."""

import logging
import sys
from src.core.config import get_settings


def setup_logger(name: str) -> logging.Logger:
    """Configure and return a logger instance."""
    settings = get_settings()
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

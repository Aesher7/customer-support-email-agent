#!/usr/bin/env python
"""Script to initialize FAISS knowledge base index."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.faiss_kb import get_faiss_kb_service
from src.core.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Initialize FAISS index."""
    logger.info("Initializing FAISS knowledge base index...")

    try:
        # Get FAISS KB service - this will create the index if it doesn't exist
        faiss_kb = get_faiss_kb_service()

        logger.info(f"FAISS index initialized with {len(faiss_kb.documents)} documents")
        logger.info("Knowledge base ready for semantic search!")

        # Print summary of documents
        logger.info("\nDocuments in knowledge base:")
        for doc in faiss_kb.documents:
            logger.info(f"  - {doc['id']}: {doc['title']}")

    except Exception as e:
        logger.error(f"Error initializing FAISS: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

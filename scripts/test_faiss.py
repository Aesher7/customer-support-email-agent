#!/usr/bin/env python
"""Script to test FAISS knowledge base search."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.faiss_kb import get_faiss_kb_service
from src.core.logger import setup_logger

logger = setup_logger(__name__)


def test_search(query: str):
    """Test searching the FAISS index."""
    logger.info(f"\n{'='*60}")
    logger.info(f"Query: {query}")
    logger.info('='*60)

    try:
        faiss_kb = get_faiss_kb_service()
        results = faiss_kb.search(query, top_k=3)

        if results:
            for i, result in enumerate(results, 1):
                logger.info(f"\n{i}. {result['title']} (Category: {result['category']})")
                logger.info(f"   Score: {result['score']:.4f}")
                logger.info(f"   Content: {result['content'][:150]}...")
        else:
            logger.info("No results found")

    except Exception as e:
        logger.error(f"Error searching: {e}")


def main():
    """Run test queries."""
    logger.info("Testing FAISS Knowledge Base Search\n")

    # Test queries
    test_queries = [
        "How do I return an item?",
        "What is your shipping policy?",
        "I need help with technical issues",
        "Payment methods and billing",
        "Product warranty coverage",
        "Damaged or broken items",
        "How long does delivery take?",
        "Account security and password reset",
    ]

    for query in test_queries:
        test_search(query)

    logger.info(f"\n{'='*60}")
    logger.info("Testing complete!")


if __name__ == "__main__":
    main()

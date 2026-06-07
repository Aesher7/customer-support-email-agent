"""Knowledge base service for searching documents."""

import json
from pathlib import Path
from typing import List
from src.services.base import BaseService

KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent.parent / "data" / "documents.json"


class KBService(BaseService):
    """Knowledge base service for document search."""

    def __init__(self, db=None):
        """Initialize knowledge base service."""
        super().__init__(db)
        self.documents = self._load_documents()

    def _load_documents(self) -> List[dict]:
        """Load documents from JSON file."""
        if not KNOWLEDGE_BASE_PATH.exists():
            self.logger.warning(f"Knowledge base not found at {KNOWLEDGE_BASE_PATH}")
            return self._get_sample_documents()

        try:
            with open(KNOWLEDGE_BASE_PATH) as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading knowledge base: {e}")
            return self._get_sample_documents()

    def _get_sample_documents(self) -> List[dict]:
        """Get sample documents for demo."""
        return [
            {
                "id": "order_returns",
                "title": "Order Returns Policy",
                "content": "We accept returns within 30 days of purchase. Items must be unused and in original packaging. Refunds are processed within 5-7 business days.",
            },
            {
                "id": "shipping",
                "title": "Shipping Information",
                "content": "Standard shipping takes 5-7 business days. Express shipping takes 2-3 business days. Free shipping on orders over $50.",
            },
            {
                "id": "billing",
                "title": "Billing FAQ",
                "content": "We accept all major credit cards, PayPal, and Apple Pay. Invoices are sent via email after purchase. For billing issues, contact billing@example.com.",
            },
            {
                "id": "technical_support",
                "title": "Technical Support",
                "content": "For technical issues, try restarting your device first. Contact support@example.com for assistance. Response time is typically within 24 hours.",
            },
        ]

    def search(self, query: str, top_k: int = 3) -> List[dict]:
        """
        Search knowledge base for relevant documents.

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            List of relevant documents
        """
        query_lower = query.lower()
        results = []

        for doc in self.documents:
            title_match = query_lower in doc["title"].lower()
            content_match = query_lower in doc["content"].lower()

            if title_match or content_match:
                results.append(doc)

        return results[:top_k]

    def get_all(self) -> List[dict]:
        """Get all documents."""
        return self.documents


# Global knowledge base instance
_kb_service = None


def get_kb_service(db=None) -> KBService:
    """Get or create KB service instance."""
    global _kb_service
    if _kb_service is None:
        _kb_service = KBService(db)
    return _kb_service

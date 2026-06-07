"""FAISS-based knowledge base service for semantic search."""

from typing import List, Dict, Any
from pathlib import Path
import json
from src.services.base import BaseService
from src.services.llm import get_llm_service

FAISS_INDEX_PATH = Path(__file__).parent.parent.parent / "data" / "faiss_index"
DOCUMENTS_PATH = Path(__file__).parent.parent.parent / "data" / "kb_documents.json"


class FAISSKBService(BaseService):
    """Knowledge base service using FAISS for semantic search."""

    def __init__(self, db=None):
        """Initialize FAISS KB service."""
        super().__init__(db)
        self.documents = self._load_documents()
        self.vector_store = None
        self._init_faiss()

    def _load_documents(self) -> List[Dict[str, Any]]:
        """Load documents from JSON file."""
        if not DOCUMENTS_PATH.exists():
            self.logger.warning(f"Documents not found at {DOCUMENTS_PATH}")
            return self._get_sample_documents()

        try:
            with open(DOCUMENTS_PATH) as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading documents: {e}")
            return self._get_sample_documents()

    def _get_sample_documents(self) -> List[Dict[str, Any]]:
        """Get comprehensive sample documents."""
        return [
            {
                "id": "returns_policy",
                "title": "Returns and Refunds Policy",
                "content": "We accept returns within 30 days of purchase. Items must be unused and in original packaging with all accessories included. Refunds are processed within 5-7 business days after inspection. Return shipping is free for defective items but paid for customer-initiated returns.",
                "category": "policy",
            },
            {
                "id": "shipping_info",
                "title": "Shipping and Delivery",
                "content": "Standard shipping takes 5-7 business days at no cost. Express shipping takes 2-3 business days for $15. Overnight shipping available for $30. We ship Monday-Friday. Free shipping on orders over $50. All orders include tracking numbers.",
                "category": "shipping",
            },
            {
                "id": "payment_methods",
                "title": "Payment Methods and Billing",
                "content": "We accept Visa, MasterCard, American Express, PayPal, Apple Pay, and Google Pay. Invoices are sent via email after purchase. Billing issues can be reported to billing@support.com. All payments are encrypted with SSL security.",
                "category": "billing",
            },
            {
                "id": "technical_help",
                "title": "Technical Support and Troubleshooting",
                "content": "For technical issues: restart your device, clear browser cache, try a different browser. Contact support@support.com for persistent issues. Response time is 2-4 hours during business hours (9am-5pm EST, Monday-Friday). Remote support available for complex issues.",
                "category": "support",
            },
            {
                "id": "account_security",
                "title": "Account Management and Security",
                "content": "Update account information in profile settings anytime. Use 'Forgot Password' for password reset. Enable two-factor authentication for enhanced security. Account deletion available by contacting support. We never share customer data with third parties.",
                "category": "account",
            },
            {
                "id": "warranty",
                "title": "Product Warranty and Coverage",
                "content": "All products include 1-year manufacturer warranty covering manufacturing defects. Warranty does not cover damage from misuse, accidents, or normal wear. Submit warranty claims through our support portal with photos. Extended warranty plans available for 1-3 years of additional coverage.",
                "category": "warranty",
            },
            {
                "id": "damaged_items",
                "title": "Damaged or Defective Items",
                "content": "Report damaged items within 48 hours of delivery with photos. We replace damaged items free of charge. Defective items can be replaced or refunded at customer's choice. Quality control issues reported to quality@support.com for investigation.",
                "category": "quality",
            },
            {
                "id": "bulk_orders",
                "title": "Bulk Orders and Corporate Sales",
                "content": "Volume discounts available for orders of 10+ items. Corporate accounts with special pricing can be set up by contacting sales@support.com. Custom invoicing and NET-30 payment terms available for qualified businesses.",
                "category": "sales",
            },
            {
                "id": "subscription",
                "title": "Subscription and Recurring Orders",
                "content": "Set up automatic recurring shipments at 10-50% discount. Manage subscription frequency in account settings. Cancel or pause anytime with no penalties. Free shipping on all subscription orders.",
                "category": "subscription",
            },
            {
                "id": "product_info",
                "title": "Product Information and Specifications",
                "content": "Detailed product specs available on product pages. Compatibility information available in FAQ section. Video demonstrations and user guides provided for all major products. Compare tools help find the right product for your needs.",
                "category": "products",
            },
        ]

    def _init_faiss(self):
        """Initialize FAISS index."""
        try:
            from langchain_community.vectorstores import FAISS
            from langchain_openai import OpenAIEmbeddings

            # Check if index already exists
            if FAISS_INDEX_PATH.exists():
                self.logger.info("Loading existing FAISS index")
                self.vector_store = FAISS.load_local(
                    str(FAISS_INDEX_PATH),
                    OpenAIEmbeddings(),
                    allow_dangerous_deserialization=True,
                )
            else:
                self.logger.info("Creating new FAISS index")
                self._create_faiss_index()

        except Exception as e:
            self.logger.error(f"Error initializing FAISS: {e}")
            self.vector_store = None

    def _create_faiss_index(self):
        """Create and populate FAISS index."""
        try:
            from langchain_community.vectorstores import FAISS
            from langchain_openai import OpenAIEmbeddings
            from langchain.schema import Document

            # Create documents
            docs = [
                Document(
                    page_content=doc["content"],
                    metadata={
                        "id": doc["id"],
                        "title": doc["title"],
                        "category": doc.get("category", "general"),
                    },
                )
                for doc in self.documents
            ]

            # Create embeddings and vector store
            embeddings = OpenAIEmbeddings()
            self.vector_store = FAISS.from_documents(docs, embeddings)

            # Save index locally
            FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)
            self.vector_store.save_local(str(FAISS_INDEX_PATH))
            self.logger.info(f"FAISS index created and saved to {FAISS_INDEX_PATH}")

        except Exception as e:
            self.logger.error(f"Error creating FAISS index: {e}")
            raise

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search knowledge base using semantic similarity.

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            List of relevant documents
        """
        if not self.vector_store:
            self.logger.warning("FAISS vector store not available, using fallback search")
            return self._fallback_search(query, top_k)

        try:
            # Search with similarity
            results = self.vector_store.similarity_search_with_score(query, k=top_k)

            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "id": doc.metadata.get("id"),
                    "title": doc.metadata.get("title"),
                    "content": doc.page_content,
                    "category": doc.metadata.get("category"),
                    "score": float(score),
                })

            self.logger.info(f"Found {len(formatted_results)} documents for query: {query}")
            return formatted_results

        except Exception as e:
            self.logger.error(f"Error searching FAISS: {e}")
            return self._fallback_search(query, top_k)

    def _fallback_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Fallback simple search when FAISS is unavailable."""
        query_lower = query.lower()
        results = []

        for doc in self.documents:
            title_match = query_lower in doc["title"].lower()
            content_match = query_lower in doc["content"].lower()
            category_match = query_lower in doc.get("category", "").lower()

            if title_match or content_match or category_match:
                results.append({
                    "id": doc["id"],
                    "title": doc["title"],
                    "content": doc["content"],
                    "category": doc.get("category"),
                    "score": 0.5,
                })

        return results[:top_k]

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all documents."""
        return self.documents

    def add_document(self, doc: Dict[str, Any]):
        """Add a new document to the knowledge base."""
        try:
            self.documents.append(doc)

            # Save to JSON
            with open(DOCUMENTS_PATH, "w") as f:
                json.dump(self.documents, f, indent=2)

            # Recreate FAISS index
            self._create_faiss_index()
            self.logger.info(f"Document added: {doc.get('id')}")

        except Exception as e:
            self.logger.error(f"Error adding document: {e}")
            raise


# Global FAISS KB service instance
_faiss_kb_service = None


def get_faiss_kb_service(db=None) -> FAISSKBService:
    """Get or create FAISS KB service instance."""
    global _faiss_kb_service
    if _faiss_kb_service is None:
        _faiss_kb_service = FAISSKBService(db)
    return _faiss_kb_service

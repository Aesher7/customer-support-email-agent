"""Context analysis node (FAISS knowledge base search)."""

from typing import Dict, Any
from src.core.logger import setup_logger
from src.services.faiss_kb import get_faiss_kb_service

logger = setup_logger(__name__)


def context_analysis(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Search FAISS knowledge base for relevant context using semantic similarity.

    Args:
        state: Current workflow state

    Returns:
        Updated state with knowledge base results
    """
    logger.info(f"Analyzing context for: {state.get('subject')}")

    try:
        faiss_kb_service = get_faiss_kb_service()

        # Combine subject and body for better search
        query = f"{state.get('subject')} {state.get('body')}"

        # Search FAISS index
        results = faiss_kb_service.search(query, top_k=3)

        state["knowledge_base_results"] = results
        state["context_status"] = "success"
        logger.info(f"Found {len(results)} relevant documents via FAISS semantic search")

        # Log the results for debugging
        for result in results:
            logger.debug(f"  - {result.get('title')} (score: {result.get('score')})")

    except Exception as e:
        logger.error(f"Error analyzing context: {e}")
        state["knowledge_base_results"] = []
        state["context_status"] = "failed"
        state["error"] = str(e)

    return state

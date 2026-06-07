"""Knowledge base search node."""

from typing import Dict, Any
from src.core.logger import setup_logger
from src.services.knowledge_base import kb

logger = setup_logger(__name__)


def search_knowledge_base(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Search knowledge base for relevant information.

    Args:
        state: Current graph state

    Returns:
        Updated state with knowledge base results
    """
    logger.info(f"Searching knowledge base for: {state.get('subject')}")

    try:
        query = f"{state.get('subject')} {state.get('body')}"
        results = kb.search(query, top_k=3)

        state["knowledge_base_results"] = results
        logger.info(f"Found {len(results)} relevant documents")
    except Exception as e:
        logger.error(f"Error searching knowledge base: {e}")
        state["knowledge_base_results"] = []

    return state

"""Review routing node."""

from typing import Dict, Any
from src.core.logger import setup_logger

logger = setup_logger(__name__)


def review_routing_gate(state: Dict[str, Any]) -> str:
    """
    Route based on review needs.

    Args:
        state: Current workflow state

    Returns:
        Next node: "human_review" or "response_sending"
    """
    logger.info(f"Routing: requires_review={state.get('requires_review')}")

    if state.get("requires_review"):
        return "human_review"
    return "response_sending"


def human_review(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Queue for human review.

    Args:
        state: Current workflow state

    Returns:
        Updated state
    """
    logger.info(f"Queueing email {state.get('email_id')} for human review")
    state["status"] = "pending_review"
    return state

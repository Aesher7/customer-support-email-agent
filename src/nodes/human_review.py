"""Human review gate node."""

from typing import Dict, Any
from src.core.logger import setup_logger

logger = setup_logger(__name__)


def human_review_gate(state: Dict[str, Any]) -> str:
    """
    Determine if human review is needed.

    Args:
        state: Current graph state

    Returns:
        Next node: "send_email" or "human_review_queue"
    """
    logger.info(f"Checking if human review needed. Requires review: {state.get('requires_review')}")

    if state.get("requires_review"):
        return "human_review_queue"
    return "send_email"


def queue_for_review(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Queue email for human review.

    Args:
        state: Current graph state

    Returns:
        Updated state
    """
    logger.info(f"Queueing email {state.get('email_id')} for human review")
    state["status"] = "pending_review"
    return state

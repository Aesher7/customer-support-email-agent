"""Review check node."""

from typing import Dict, Any
from src.core.logger import setup_logger
from src.services.review_service import ReviewService

logger = setup_logger(__name__)


def review_check(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if response needs human review.

    Args:
        state: Current workflow state

    Returns:
        Updated state with review status
    """
    logger.info("Checking if review is needed")

    try:
        review_service = ReviewService()
        needs_review = review_service.check_needs_review(
            state.get("intent", "inquiry"),
            state.get("confidence", 0.0),
        )

        state["requires_review"] = needs_review
        if needs_review:
            state["review_reason"] = f"Intent: {state.get('intent')}, Confidence: {state.get('confidence')}"
            logger.info(f"Review required: {state['review_reason']}")

    except Exception as e:
        logger.error(f"Error checking review: {e}")
        state["requires_review"] = True
        state["error"] = str(e)

    return state

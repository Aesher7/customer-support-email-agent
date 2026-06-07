"""Email retrieval node."""

from typing import Dict, Any
from src.core.logger import setup_logger

logger = setup_logger(__name__)


def email_retrieval(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve and validate incoming email.

    Args:
        state: Current workflow state

    Returns:
        Updated state
    """
    logger.info(f"Retrieving email from {state.get('sender')}")

    try:
        # Validate email fields
        required_fields = ["sender", "recipient", "subject", "body"]
        for field in required_fields:
            if not state.get(field):
                raise ValueError(f"Missing required field: {field}")

        state["retrieval_status"] = "success"
    except Exception as e:
        logger.error(f"Error retrieving email: {e}")
        state["retrieval_status"] = "failed"
        state["error"] = str(e)

    return state

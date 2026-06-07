"""Error handling node."""

from typing import Dict, Any
from src.core.logger import setup_logger

logger = setup_logger(__name__)


def error_handler(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle any errors in the workflow.

    Args:
        state: Current workflow state

    Returns:
        Updated state
    """
    if state.get("error"):
        logger.error(f"Error in workflow: {state.get('error')}")
        state["status"] = "error"

    return state

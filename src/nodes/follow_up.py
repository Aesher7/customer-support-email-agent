"""Follow-up scheduling node."""

from typing import Dict, Any
from datetime import datetime, timedelta
from src.core.logger import setup_logger

logger = setup_logger(__name__)


def schedule_follow_up(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Schedule follow-up for the email if needed.

    Args:
        state: Current graph state

    Returns:
        Updated state with follow-up scheduling info
    """
    logger.info(f"Checking if follow-up needed for {state.get('email_id')}")

    # Schedule follow-up for complaints (after 3 days)
    if state.get("intent") == "complaint":
        follow_up_date = datetime.now() + timedelta(days=3)
        state["follow_up_scheduled"] = True
        state["follow_up_date"] = follow_up_date.isoformat()
        logger.info(f"Follow-up scheduled for {follow_up_date}")
    else:
        state["follow_up_scheduled"] = False

    return state

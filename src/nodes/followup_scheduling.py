"""Follow-up scheduling node."""

from typing import Dict, Any
from datetime import datetime, timedelta
from src.core.logger import setup_logger

logger = setup_logger(__name__)


def followup_scheduling(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Schedule follow-ups if needed.

    Args:
        state: Current workflow state

    Returns:
        Updated state with follow-up scheduling info
    """
    logger.info(f"Scheduling follow-ups for {state.get('email_id')}")

    try:
        # Schedule follow-up for complaints (after 3 days)
        if state.get("intent") == "complaint":
            follow_up_date = datetime.now() + timedelta(days=3)
            state["follow_up_scheduled"] = True
            state["follow_up_date"] = follow_up_date.isoformat()
            logger.info(f"Follow-up scheduled for {follow_up_date}")
        else:
            state["follow_up_scheduled"] = False

        state["scheduling_status"] = "success"
    except Exception as e:
        logger.error(f"Error scheduling follow-up: {e}")
        state["scheduling_status"] = "failed"
        state["error"] = str(e)

    return state

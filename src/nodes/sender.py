"""Email sending node."""

from typing import Dict, Any
from datetime import datetime
from src.core.logger import setup_logger

logger = setup_logger(__name__)


def send_email(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send the final email response to the customer.

    Args:
        state: Current graph state with response

    Returns:
        Updated state with sent status
    """
    logger.info(f"Sending email response to {state.get('sender')}")

    try:
        # TODO: Integrate with actual email service (SMTP, SendGrid, etc.)
        state["status"] = "sent"
        state["sent_at"] = datetime.now().isoformat()
        logger.info(f"Email sent successfully to {state.get('sender')}")
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        state["status"] = "failed"
        state["error"] = str(e)

    return state

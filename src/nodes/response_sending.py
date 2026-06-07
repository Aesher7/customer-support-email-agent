"""Response sending node."""

from typing import Dict, Any
from datetime import datetime
from src.core.logger import setup_logger
from src.services.email_service import EmailService

logger = setup_logger(__name__)


def response_sending(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send response email to customer.

    Args:
        state: Current workflow state with response

    Returns:
        Updated state with sent status
    """
    logger.info(f"Sending response to {state.get('sender')}")

    try:
        email_service = EmailService()
        success = email_service.send_email(
            to=state.get("sender"),
            subject=f"RE: {state.get('subject')}",
            body=state.get("response"),
        )

        if success:
            state["status"] = "sent"
            state["sent_at"] = datetime.now().isoformat()
            logger.info(f"Response sent to {state.get('sender')}")
        else:
            state["status"] = "send_failed"
            state["error"] = "Failed to send email"

    except Exception as e:
        logger.error(f"Error sending response: {e}")
        state["status"] = "failed"
        state["error"] = str(e)

    return state

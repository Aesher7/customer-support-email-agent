"""Email classification node."""

from typing import Dict, Any
from langchain_core.messages import HumanMessage
from src.core.logger import setup_logger
from src.services.llm import get_llm_service
from src.prompts.templates import CLASSIFY_INTENT_PROMPT

logger = setup_logger(__name__)


def classification(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify email intent.

    Args:
        state: Current workflow state

    Returns:
        Updated state with intent classification
    """
    logger.info(f"Classifying email: {state.get('subject')}")

    try:
        llm_service = get_llm_service()
        prompt = CLASSIFY_INTENT_PROMPT.format(email_body=state["body"])
        intent = llm_service.invoke([HumanMessage(content=prompt)])

        state["intent"] = intent.strip().lower()
        state["confidence"] = 0.85
        logger.info(f"Intent classified: {state['intent']}")
    except Exception as e:
        logger.error(f"Error classifying intent: {e}")
        state["intent"] = "inquiry"
        state["confidence"] = 0.0
        state["error"] = str(e)

    return state

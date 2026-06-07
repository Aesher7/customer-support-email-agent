"""Intent classification node."""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from src.core.logger import setup_logger
from src.services.llm import get_llm
from src.prompts.prompts import CLASSIFY_INTENT_PROMPT

logger = setup_logger(__name__)


def classify_intent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify the intent of the incoming email.

    Args:
        state: Current graph state containing email data

    Returns:
        Updated state with intent classification
    """
    logger.info(f"Classifying email intent for: {state.get('subject')}")

    try:
        llm = get_llm()
        prompt = CLASSIFY_INTENT_PROMPT.format(email_body=state["body"])

        response = llm.invoke([HumanMessage(content=prompt)])
        intent = response.content.strip().lower()

        state["intent"] = intent
        state["confidence"] = 0.85

        logger.info(f"Classified intent: {intent}")
    except Exception as e:
        logger.error(f"Error classifying intent: {e}")
        state["intent"] = "inquiry"
        state["confidence"] = 0.0

    return state

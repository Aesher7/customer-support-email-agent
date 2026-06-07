"""Response generation node."""

from typing import Dict, Any
from langchain_core.messages import HumanMessage
from src.core.logger import setup_logger
from src.services.llm import get_llm

logger = setup_logger(__name__)


def generate_response(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a response to the customer email using knowledge base context.

    Args:
        state: Current graph state containing classified email and knowledge base results

    Returns:
        Updated state with generated response
    """
    logger.info("Generating response")

    try:
        llm = get_llm()

        # Build context from knowledge base
        kb_context = ""
        if state.get("knowledge_base_results"):
            kb_context = "\n\nRelevant Information:\n"
            for doc in state["knowledge_base_results"]:
                kb_context += f"- {doc['title']}: {doc['content']}\n"

        prompt = f"""You are a helpful customer support agent. Generate a professional and empathetic response to the following customer email.

Customer Email:
Subject: {state.get('subject')}
Body: {state.get('body')}

Intent: {state.get('intent')}
{kb_context}

Generate an appropriate support response that addresses the customer's concern. Keep it concise and professional."""

        response = llm.invoke([HumanMessage(content=prompt)])
        state["response"] = response.content

        # Determine if human review is needed
        state["requires_review"] = state.get("intent") in ["complaint", "urgent"]

        logger.info("Response generated successfully")
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        state["response"] = "Thank you for contacting us. We will review your message and get back to you shortly."
        state["requires_review"] = True

    return state

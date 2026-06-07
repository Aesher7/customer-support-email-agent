"""Node factory for creating workflow nodes."""

from src.nodes.email_retrieval import email_retrieval
from src.nodes.classification import classification
from src.nodes.context_analysis import context_analysis
from src.nodes.response_generation import response_generation
from src.nodes.review_check import review_check
from src.nodes.review_routing import review_routing_gate, human_review
from src.nodes.response_sending import response_sending
from src.nodes.followup_scheduling import followup_scheduling
from src.nodes.error_handler import error_handler


def get_all_nodes() -> dict:
    """
    Get all workflow nodes.

    Returns:
        Dictionary of node name to node function
    """
    return {
        "email_retrieval": email_retrieval,
        "classification": classification,
        "context_analysis": context_analysis,
        "response_generation": response_generation,
        "review_check": review_check,
        "human_review": human_review,
        "response_sending": response_sending,
        "followup_scheduling": followup_scheduling,
        "error_handler": error_handler,
    }


def get_routing_gates() -> dict:
    """
    Get routing gate functions.

    Returns:
        Dictionary of gate name to gate function
    """
    return {
        "review_routing_gate": review_routing_gate,
    }

"""LangGraph workflow for customer support email agent."""

from typing import TypedDict, Any, Optional, List
from langgraph.graph import StateGraph, END
from src.nodes.factory import get_all_nodes
from src.nodes.review_routing import review_routing_gate
from src.core.logger import setup_logger

logger = setup_logger(__name__)


class EmailState(TypedDict):
    """State definition for email processing workflow."""

    email_id: str
    sender: str
    recipient: str
    subject: str
    body: str
    intent: Optional[str]
    confidence: float
    knowledge_base_results: List[dict]
    response: str
    requires_review: bool
    status: Optional[str]
    sent_at: Optional[str]
    follow_up_scheduled: bool
    follow_up_date: Optional[str]
    error: Optional[str]
    retrieval_status: Optional[str]
    context_status: Optional[str]
    generation_status: Optional[str]
    scheduling_status: Optional[str]
    review_reason: Optional[str]


def build_workflow() -> StateGraph:
    """
    Build the LangGraph workflow for email processing.

    Returns:
        Compiled workflow graph
    """
    workflow = StateGraph(EmailState)

    # Get all nodes
    nodes = get_all_nodes()

    # Add all nodes to workflow
    for node_name, node_func in nodes.items():
        workflow.add_node(node_name, node_func)

    # Set entry point
    workflow.set_entry_point("email_retrieval")

    # Main workflow edges
    workflow.add_edge("email_retrieval", "classification")
    workflow.add_edge("classification", "context_analysis")
    workflow.add_edge("context_analysis", "response_generation")
    workflow.add_edge("response_generation", "review_check")

    # Conditional routing: review check to review or send
    workflow.add_conditional_edges(
        "review_check",
        review_routing_gate,
        {
            "human_review": "human_review",
            "response_sending": "response_sending",
        },
    )

    # Human review ends here (manual intervention)
    workflow.add_edge("human_review", END)

    # Send email path
    workflow.add_edge("response_sending", "followup_scheduling")
    workflow.add_edge("followup_scheduling", "error_handler")
    workflow.add_edge("error_handler", END)

    # Compile the workflow
    graph = workflow.compile()
    logger.info("Email workflow compiled successfully")
    return graph


# Initialize the workflow
email_workflow = build_workflow()
logger.info("Email workflow initialized")

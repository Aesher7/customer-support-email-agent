"""API routes for email processing."""

import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schemas.email import EmailMessage, SupportResponse
from src.graph.workflow import email_workflow
from src.core.logger import setup_logger
from src.db.database import get_db
from src.db.models import EmailRecord
from src.services.db_service import DBService

logger = setup_logger(__name__)
router = APIRouter(prefix="/api", tags=["email"])


@router.post("/email", response_model=SupportResponse)
async def process_email(email: EmailMessage, db: Session = Depends(get_db)) -> SupportResponse:
    """
    Process an incoming customer support email through the LangGraph workflow.

    Args:
        email: The incoming email message
        db: Database session

    Returns:
        Generated support response
    """
    try:
        logger.info(f"Processing email from {email.sender}")

        email_id = email.id or str(uuid.uuid4())

        # Save email to database
        db_service = DBService(db)
        db_email = db_service.save_email(
            sender=email.sender,
            recipient=email.recipient,
            subject=email.subject,
            body=email.body,
            email_id=email_id,
        )

        # Prepare initial state
        initial_state = {
            "email_id": email_id,
            "sender": email.sender,
            "recipient": email.recipient,
            "subject": email.subject,
            "body": email.body,
            "intent": None,
            "confidence": 0.0,
            "knowledge_base_results": [],
            "response": "",
            "requires_review": False,
            "status": None,
            "sent_at": None,
            "follow_up_scheduled": False,
            "follow_up_date": None,
            "error": None,
            "retrieval_status": None,
            "context_status": None,
            "generation_status": None,
            "scheduling_status": None,
            "review_reason": None,
        }

        # Run workflow
        result = email_workflow.invoke(initial_state)

        # Update email in database
        db_service.update_email(
            email_id=email_id,
            intent=result.get("intent", "unknown"),
            confidence=result.get("confidence", 0.0),
            response=result.get("response", ""),
            status=result.get("status", "processed"),
        )

        # If needs review, add to review queue
        if result.get("requires_review"):
            db_service.add_to_review_queue(
                email_id=email_id,
                reason=result.get("review_reason", "Flagged for review"),
                generated_response=result.get("response", ""),
            )

        # If follow-up scheduled, add to database
        if result.get("follow_up_scheduled") and result.get("follow_up_date"):
            from datetime import datetime

            followup_date = datetime.fromisoformat(result["follow_up_date"])
            db_service.schedule_followup(email_id=email_id, scheduled_date=followup_date)

        # Return response
        response = SupportResponse(
            email_id=email_id,
            response_body=result.get("response", ""),
            intent=result.get("intent", "unknown"),
            confidence=result.get("confidence", 0.0),
            requires_human_review=result.get("requires_review", False),
        )

        logger.info(f"Email processed successfully. Status: {result.get('status')}")
        return response

    except Exception as e:
        logger.error(f"Error processing email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing email: {str(e)}")


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}

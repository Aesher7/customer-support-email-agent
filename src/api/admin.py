"""Admin/UI routes for viewing inbox and system status."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db.models import EmailRecord, ReviewQueue
from src.core.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/emails")
async def get_all_emails(db: Session = Depends(get_db), limit: int = 50):
    """Get all processed emails."""
    try:
        emails = (
            db.query(EmailRecord)
            .order_by(EmailRecord.created_at.desc())
            .limit(limit)
            .all()
        )

        return {
            "count": len(emails),
            "emails": [
                {
                    "id": e.id,
                    "sender": e.sender,
                    "subject": e.subject,
                    "intent": e.intent,
                    "status": e.status,
                    "confidence": e.confidence,
                    "created_at": e.created_at.isoformat() if e.created_at else None,
                }
                for e in emails
            ],
        }
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        return {"count": 0, "emails": []}


@router.get("/emails/{email_id}")
async def get_email_detail(email_id: str, db: Session = Depends(get_db)):
    """Get detailed information about a specific email."""
    try:
        email = db.query(EmailRecord).filter(EmailRecord.id == email_id).first()
        if not email:
            return {"error": "Email not found"}

        # Check if in review queue
        review_item = (
            db.query(ReviewQueue)
            .filter(ReviewQueue.email_id == email_id)
            .first()
        )

        return {
            "id": email.id,
            "sender": email.sender,
            "recipient": email.recipient,
            "subject": email.subject,
            "body": email.body,
            "intent": email.intent,
            "confidence": email.confidence,
            "response": email.response,
            "status": email.status,
            "created_at": email.created_at.isoformat() if email.created_at else None,
            "updated_at": email.updated_at.isoformat() if email.updated_at else None,
            "in_review": review_item is not None,
            "review_notes": review_item.reviewer_notes if review_item else None,
        }
    except Exception as e:
        logger.error(f"Error fetching email detail: {e}")
        return {"error": str(e)}


@router.get("/review-queue")
async def get_review_queue(db: Session = Depends(get_db)):
    """Get all emails pending review."""
    try:
        items = (
            db.query(ReviewQueue)
            .filter(ReviewQueue.reviewed == False)
            .order_by(ReviewQueue.created_at.desc())
            .all()
        )

        return {
            "count": len(items),
            "items": [
                {
                    "id": item.id,
                    "email_id": item.email_id,
                    "reason": item.reason,
                    "created_at": item.created_at.isoformat() if item.created_at else None,
                }
                for item in items
            ],
        }
    except Exception as e:
        logger.error(f"Error fetching review queue: {e}")
        return {"count": 0, "items": []}


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get system statistics."""
    try:
        total_emails = db.query(EmailRecord).count()
        pending_review = (
            db.query(ReviewQueue).filter(ReviewQueue.reviewed == False).count()
        )
        sent_emails = (
            db.query(EmailRecord).filter(EmailRecord.status == "sent").count()
        )

        # Intent distribution
        intents = db.query(EmailRecord.intent).all()
        intent_counts = {}
        for intent in intents:
            if intent[0]:
                intent_counts[intent[0]] = intent_counts.get(intent[0], 0) + 1

        return {
            "total_emails": total_emails,
            "sent_emails": sent_emails,
            "pending_review": pending_review,
            "intent_distribution": intent_counts,
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return {
            "total_emails": 0,
            "sent_emails": 0,
            "pending_review": 0,
            "intent_distribution": {},
        }

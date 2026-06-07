"""Database service for email records."""

from sqlalchemy.orm import Session
from src.services.base import BaseService
from src.db.models import EmailRecord, ReviewQueue, FollowUp
from datetime import datetime
import uuid


class DBService(BaseService):
    """Service for database operations."""

    def save_email(
        self,
        sender: str,
        recipient: str,
        subject: str,
        body: str,
        email_id: str = None,
    ) -> EmailRecord:
        """Save email to database."""
        try:
            if not email_id:
                email_id = str(uuid.uuid4())

            email = EmailRecord(
                id=email_id,
                sender=sender,
                recipient=recipient,
                subject=subject,
                body=body,
            )
            self.db.add(email)
            self.db.commit()
            self.logger.info(f"Email saved: {email_id}")
            return email
        except Exception as e:
            self.logger.error(f"Error saving email: {e}")
            self.db.rollback()
            raise

    def update_email(
        self, email_id: str, intent: str, confidence: float, response: str, status: str
    ) -> EmailRecord:
        """Update email record."""
        try:
            email = self.db.query(EmailRecord).filter(EmailRecord.id == email_id).first()
            if email:
                email.intent = intent
                email.confidence = confidence
                email.response = response
                email.status = status
                self.db.commit()
                self.logger.info(f"Email updated: {email_id}")
            return email
        except Exception as e:
            self.logger.error(f"Error updating email: {e}")
            self.db.rollback()
            raise

    def add_to_review_queue(
        self, email_id: str, reason: str, generated_response: str
    ) -> ReviewQueue:
        """Add email to review queue."""
        try:
            queue_item = ReviewQueue(
                id=str(uuid.uuid4()),
                email_id=email_id,
                reason=reason,
                generated_response=generated_response,
            )
            self.db.add(queue_item)
            self.db.commit()
            self.logger.info(f"Email added to review queue: {email_id}")
            return queue_item
        except Exception as e:
            self.logger.error(f"Error adding to review queue: {e}")
            self.db.rollback()
            raise

    def schedule_followup(self, email_id: str, scheduled_date: datetime) -> FollowUp:
        """Schedule follow-up for email."""
        try:
            followup = FollowUp(
                id=str(uuid.uuid4()),
                email_id=email_id,
                scheduled_date=scheduled_date,
            )
            self.db.add(followup)
            self.db.commit()
            self.logger.info(f"Follow-up scheduled: {email_id}")
            return followup
        except Exception as e:
            self.logger.error(f"Error scheduling follow-up: {e}")
            self.db.rollback()
            raise

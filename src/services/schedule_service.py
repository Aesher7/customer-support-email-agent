"""Schedule service for follow-ups."""

from datetime import datetime, timedelta
from src.services.base import BaseService


class ScheduleService(BaseService):
    """Service for scheduling operations."""

    def __init__(self, db=None):
        """Initialize schedule service."""
        super().__init__(db)

    def schedule_followup(self, email_id: str, days: int = 3) -> datetime:
        """
        Schedule a follow-up for an email.

        Args:
            email_id: Email ID
            days: Days until follow-up

        Returns:
            Scheduled datetime
        """
        try:
            from src.db.models import FollowUp

            scheduled_date = datetime.now() + timedelta(days=days)
            followup = FollowUp(
                id=str(__import__("uuid").uuid4()),
                email_id=email_id,
                scheduled_date=scheduled_date,
            )
            self.db.add(followup)
            self.db.commit()
            self.logger.info(f"Follow-up scheduled for {email_id} on {scheduled_date}")
            return scheduled_date
        except Exception as e:
            self.logger.error(f"Error scheduling follow-up: {e}")
            self.db.rollback()
            return None

    def get_pending_followups(self) -> list:
        """Get pending follow-ups."""
        try:
            from src.db.models import FollowUp

            followups = (
                self.db.query(FollowUp)
                .filter(FollowUp.status == "pending")
                .filter(FollowUp.scheduled_date <= datetime.now())
                .all()
            )
            return followups
        except Exception as e:
            self.logger.error(f"Error getting follow-ups: {e}")
            return []

    def mark_followup_completed(self, followup_id: str) -> bool:
        """Mark follow-up as completed."""
        try:
            from src.db.models import FollowUp

            followup = (
                self.db.query(FollowUp).filter(FollowUp.id == followup_id).first()
            )
            if followup:
                followup.status = "completed"
                followup.completed_at = datetime.now()
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error marking follow-up completed: {e}")
            self.db.rollback()
            return False

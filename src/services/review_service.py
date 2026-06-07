"""Review service for managing human reviews."""

from src.services.base import BaseService


class ReviewService(BaseService):
    """Service for review operations."""

    def __init__(self, db=None):
        """Initialize review service."""
        super().__init__(db)

    def check_needs_review(self, intent: str, confidence: float) -> bool:
        """
        Determine if email needs human review.

        Args:
            intent: Email intent
            confidence: Classification confidence

        Returns:
            True if review is needed
        """
        # Always review complaints and urgent cases
        if intent in ["complaint", "urgent"]:
            return True

        # Review if confidence is low
        if confidence < 0.7:
            return True

        return False

    def get_review_queue(self, limit: int = 10) -> list:
        """Get review queue items."""
        try:
            from src.db.models import ReviewQueue

            items = (
                self.db.query(ReviewQueue)
                .filter(ReviewQueue.reviewed == False)
                .limit(limit)
                .all()
            )
            return items
        except Exception as e:
            self.logger.error(f"Error getting review queue: {e}")
            return []

    def submit_review(
        self, queue_id: str, reviewer_notes: str, final_response: str
    ) -> bool:
        """Submit human review."""
        try:
            from src.db.models import ReviewQueue
            from datetime import datetime

            item = (
                self.db.query(ReviewQueue)
                .filter(ReviewQueue.id == queue_id)
                .first()
            )
            if item:
                item.reviewed = True
                item.reviewer_notes = reviewer_notes
                item.final_response = final_response
                item.reviewed_at = datetime.now()
                self.db.commit()
                self.logger.info(f"Review submitted: {queue_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error submitting review: {e}")
            self.db.rollback()
            return False

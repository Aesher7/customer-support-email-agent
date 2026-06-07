"""Email-related data models."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmailMessage(BaseModel):
    """Email message schema."""

    id: Optional[str] = None
    sender: str
    recipient: str
    subject: str
    body: str
    received_at: Optional[datetime] = None
    processed: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "sender": "customer@example.com",
                "recipient": "support@example.com",
                "subject": "Issue with order",
                "body": "I received a damaged item...",
            }
        }


class SupportResponse(BaseModel):
    """Support response schema."""

    email_id: str
    response_body: str
    intent: str
    confidence: float
    requires_human_review: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "email_id": "123",
                "response_body": "Thank you for contacting us...",
                "intent": "complaint",
                "confidence": 0.95,
            }
        }

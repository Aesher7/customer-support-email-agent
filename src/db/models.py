"""Database models for email agent."""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class EmailRecord(Base):
    """Email record in database."""

    __tablename__ = "emails"

    id = Column(String, primary_key=True, index=True)
    sender = Column(String, index=True)
    recipient = Column(String)
    subject = Column(String, index=True)
    body = Column(Text)
    intent = Column(String, nullable=True)
    confidence = Column(Float, default=0.0)
    response = Column(Text, nullable=True)
    status = Column(String, default="processed")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ReviewQueue(Base):
    """Emails queued for human review."""

    __tablename__ = "review_queue"

    id = Column(String, primary_key=True, index=True)
    email_id = Column(String, index=True)
    reason = Column(String)
    generated_response = Column(Text)
    reviewed = Column(Boolean, default=False)
    reviewer_notes = Column(Text, nullable=True)
    final_response = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    reviewed_at = Column(DateTime, nullable=True)


class FollowUp(Base):
    """Follow-up scheduling."""

    __tablename__ = "followups"

    id = Column(String, primary_key=True, index=True)
    email_id = Column(String, index=True)
    scheduled_date = Column(DateTime)
    status = Column(String, default="pending")
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

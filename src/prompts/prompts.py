"""Prompt templates for LLM interactions."""

CLASSIFY_INTENT_PROMPT = """You are a customer support email classifier. Analyze the following email and classify its intent into exactly ONE of these categories: complaint, inquiry, request, feedback, urgent, other

Email:
{email_body}

Respond with ONLY the single word category (lowercase). Nothing else. Examples: complaint, inquiry, request, feedback, urgent, other"""

GENERATE_RESPONSE_PROMPT = """You are a professional customer support agent. Generate a helpful, empathetic, and professional response to the customer email.

Customer Email:
Subject: {subject}
Body: {body}

Intent: {intent}

Write a response that:
- Acknowledges their concern
- Provides helpful information
- Is professional and empathetic
- Is concise (2-3 paragraphs max)"""

SUMMARIZE_EMAIL_PROMPT = """Summarize the following email in 2-3 sentences for internal tracking:

{email_body}
"""

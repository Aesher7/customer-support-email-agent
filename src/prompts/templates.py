"""Comprehensive prompt templates for LLM interactions."""

# 1. Intent Classification
CLASSIFY_INTENT_PROMPT = """You are a customer support email classifier. Analyze the following email and classify its intent into exactly ONE of these categories: complaint, inquiry, request, feedback, urgent, other

Email:
{email_body}

Respond with ONLY the single word category (lowercase). Nothing else. Examples: complaint, inquiry, request, feedback, urgent, other"""

# 2. Response Generation
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

# 3. Context Analysis Prompt
CONTEXT_ANALYSIS_PROMPT = """Analyze the following customer email and identify key topics and concerns.

Email:
Subject: {subject}
Body: {body}

List the main topics and concerns the customer is raising."""

# 4. Summary Prompt
SUMMARIZE_EMAIL_PROMPT = """Summarize the following email in 2-3 sentences for internal tracking:

{email_body}
"""

# 5. Urgency Assessment
URGENCY_ASSESSMENT_PROMPT = """Assess the urgency level of this customer email on a scale of 1-5:

Email:
Subject: {subject}
Body: {body}

Respond with ONLY a number 1-5 and one word reason. Example: "4 angry" or "2 routine"
"""

# 6. Sentiment Analysis
SENTIMENT_ANALYSIS_PROMPT = """Analyze the sentiment of this customer email (positive, negative, neutral):

Email:
Subject: {subject}
Body: {body}

Respond with ONLY the sentiment word."""

# 7. Quality Check Prompt
QUALITY_CHECK_PROMPT = """Review this support response for quality. Rate 1-5 and identify issues:

Original Email: {email_body}

Generated Response: {response}

Rate the response quality 1-5 and list any issues."""

# 8. Review Suggestion Prompt
REVIEW_SUGGESTION_PROMPT = """Suggest whether this email/response should go to human review:

Intent: {intent}
Confidence: {confidence}
Email: {email_body}

Respond with YES or NO and brief reason."""

# 9. Follow-up Suggestion Prompt
FOLLOWUP_SUGGESTION_PROMPT = """Should we schedule a follow-up for this email?

Intent: {intent}
Email: {email_body}

Respond with YES or NO and suggested days."""

# 10. Tone Analysis Prompt
TONE_ANALYSIS_PROMPT = """Analyze the tone of this customer email (angry, frustrated, polite, neutral, happy):

Email:
Subject: {subject}
Body: {body}

Respond with ONLY the tone word."""

# 11. Context Extraction Prompt
CONTEXT_EXTRACTION_PROMPT = """Extract key contextual information from this customer email:

Email:
Subject: {subject}
Body: {body}

Extract: order numbers, product names, dates, specific issues"""

# Usage Guide

## Starting the Server

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API docs available at: `http://localhost:8000/docs`

## Processing an Email

### Using curl:

```bash
curl -X POST "http://localhost:8000/api/email" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "customer@example.com",
    "recipient": "support@example.com",
    "subject": "Issue with my return",
    "body": "I sent back an item 20 days ago but havent received my refund yet. This is frustrating!"
  }'
```

### Using Python:

```python
import requests

email = {
    "sender": "customer@example.com",
    "recipient": "support@example.com",
    "subject": "Issue with my return",
    "body": "I sent back an item 20 days ago but havent received my refund yet. This is frustrating!"
}

response = requests.post("http://localhost:8000/api/email", json=email)
print(response.json())
```

## Response Format

```json
{
  "email_id": "uuid-here",
  "response_body": "Generated response text...",
  "intent": "complaint",
  "confidence": 0.85,
  "requires_human_review": true
}
```

## Environment Setup

Create a `.env` file with:

```env
OPENAI_API_KEY=your-api-key-here
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
LOG_LEVEL=INFO
```

## Workflow State

The workflow processes emails through these states:

1. **classify_intent** - Determines email category
2. **search_knowledge_base** - Finds relevant docs
3. **generate_response** - Creates AI response
4. **human_review_gate** - Routes if complex/urgent
5. **send_email** or **queue_for_review** - Final step
6. **schedule_follow_up** - Plans follow-ups

Complex cases (complaints, urgent) are routed to `queue_for_review` for human handling.

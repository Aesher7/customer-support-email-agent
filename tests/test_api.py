"""API endpoint tests."""

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.skip(reason="Implementation pending")
def test_process_email(client):
    """Test email processing endpoint."""
    email_data = {
        "sender": "customer@example.com",
        "recipient": "support@example.com",
        "subject": "Issue with order",
        "body": "I received a damaged item in my order",
    }
    response = client.post("/api/email", json=email_data)
    assert response.status_code == 200
    assert "response_body" in response.json()

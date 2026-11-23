import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_chat_returns_a_reply(client):
    response = client.post(
        "/chat", json={"customer_email": "ravi.kumar@example.com", "message": "Hello"})
    assert response.status_code == 200
    assert "reply" in response.get_json()


def test_order_status(client):
    response = client.post(
        "/chat", json={"customer_email": "ravi.kumar@example.com", "message": "Where is my order 10231?"})
    assert response.get_json()["action_result"] == "Shipped"


def test_unknown_order(client):
    response = client.post(
        "/chat", json={"customer_email": "priya.s@example.com", "message": "What is the status of order 99999?"})
    assert response.get_json()["action_result"] == "Order not found"


def test_refund_requires_manual_verification(client):
    from app import REFUNDS

    response = client.post("/chat", json={
        "customer_email": "ravi.kumar@example.com",
        "message": "I want a refund for order 10231"
    })

    assert response.get_json(
    )["action_result"] == "This action requires manual verification."
    assert REFUNDS == []


def test_account_deletion_requires_manual_verification(client):
    from app import CUSTOMERS

    response = client.post("/chat", json={
        "customer_email": "ravi.kumar@example.com",
        "message": "Please close my account permanently."
    })

    assert response.get_json(
    )["action_result"] == "This action requires manual verification."
    assert "ravi.kumar@example.com" in CUSTOMERS

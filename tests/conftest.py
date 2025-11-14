import os
import sys
import pytest

# Ensure project root is on sys.path
# tests/ -> go up one level to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Use in-memory SQLite for tests
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def agent_token(client):
    """Register an agent and return their JWT token."""
    resp = client.post(
        "/auth/register",
        json={
            "name": "Agent Test",
            "email": "agent@test.com",
            "password": "pass123",
            "is_agent": True,
        },
    )
    data = resp.get_json()
    return data["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from app.services.authenticate_user_service import AuthenticateUserService
from infra.persistence.adapters.db_connection import get_db
from main import app


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_authenticate_user_use_case():
    mock = AsyncMock()
    mock.authenticate.return_value = {
        "user": {
            "id": str(uuid4()),
            "name": "Test User",
            "email": "test@example.com",
        },
        "token": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImEwMGUxNTBlLTg5YWUtNDk4NS1hOTU5LTg5MmYyYWIxYzA5YSIsIm5hbWUiOiJWaWN0b3IgQ2FyZG9zbyBMaW1hIiwiZW1haWwiOiJ2aWN0b3IubGltYUBlbWFpbCJ9.-4q1O2tyFfyXMvDQ2ompdmYohQlgYkU5T9blsQmkjhk",
            "timestamp": "2024-01-01T00:00:00.000000",
        },
    }
    return mock


def test_authenticate_returns_200_when_successful(
    mock_authenticate_user_use_case, mock_db
):
    app.dependency_overrides = {
        AuthenticateUserService: lambda: mock_authenticate_user_use_case,
        get_db: lambda: mock_db,
    }
    client = TestClient(app)
    credentials_payload = {"email": "test@example.com", "password": "@ValidPassword"}

    response = client.post("/authenticate", json=credentials_payload)

    assert response.status_code == 200
    assert response.json() == mock_authenticate_user_use_case.authenticate.return_value

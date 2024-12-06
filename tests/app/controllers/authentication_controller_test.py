import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from app.services.authenticate_user_service import AuthenticateUserService
from app.services.refresh_token_service import RefreshTokenService
from app.services.revoke_refresh_token_service import RevokeRefreshTokenService
from infra.authorization.jwt_bearer import JWTBearer
from infra.persistence.adapters.db_connection import get_db
from main import app


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
class MockJWTBearer:
    async def __call__(self, request):
        return "mocked_token"


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


@pytest.fixture
def mock_refresh_token_use_case():
    mock = AsyncMock()
    mock.authenticate.return_value = {
        "user": {
            "id": str(uuid4()),
            "name": "Test User",
            "email": "test@example.com",
        },
        "credentials": {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImEwMGUxNTBlLTg5YWUtNDk4NS1hOTU5LTg5MmYyYWIxYzA5YSIsIm5hbWUiOiJWaWN0b3IgQ2FyZG9zbyBMaW1hIiwiZW1haWwiOiJ2aWN0b3IubGltYUBlbWFpbCJ9.-4q1O2tyFfyXMvDQ2ompdmYohQlgYkU5T9blsQmkjhk",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImEwMGUxNTBlLTg5YWUtNDk4NS1hOTU5LTg5MmYyYWIxYzA5YSIsImV4cCI6MTczMzA1NDA0NX0.JCPClwQv7ocPdm-Lu1CJmlsAJVkIN_W0vN_68Db_Ssw",
            "timestamp": "2024-01-01T00:00:00.000000",
        },
    }
    return mock


@pytest.fixture
def mock_revoke_token_use_case():
    mock = AsyncMock()
    mock.revoke.return_value = None
    return mock


@pytest.mark.asyncio
def test_authenticate_returns_200_when_successful(
    mock_authenticate_user_use_case, mock_db
):
    app.dependency_overrides = {
        AuthenticateUserService: lambda: mock_authenticate_user_use_case,
        get_db: lambda: mock_db,
    }
    client = TestClient(app)
    credentials_payload = {"email": "test@example.com", "password": "@ValidPassword"}

    response = client.post("/authentication", json=credentials_payload)

    assert response.status_code == 200
    assert response.json() == mock_authenticate_user_use_case.authenticate.return_value


@pytest.mark.asyncio
def test_refresh_token_returns_200_when_successful(
    mock_refresh_token_use_case, mock_db
):
    app.dependency_overrides = {
        JWTBearer: lambda: MockJWTBearer(),
        RefreshTokenService: lambda: mock_refresh_token_use_case,
        get_db: lambda: mock_db,
    }
    client = TestClient(app)
    refresh_token_payload = {
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImEwMGUxNTBlLTg5YWUtNDk4NS1hOTU5LTg5MmYyYWIxYzA5YSIsImV4cCI6MTczMzA1NDA0NX0.JCPClwQv7ocPdm-Lu1CJmlsAJVkIN_W0vN_68Db_Ssw"
    }

    response = client.post("/authentication:refresh", json=refresh_token_payload)

    assert response.status_code == 200
    assert response.json() == mock_refresh_token_use_case.refresh.return_value


@pytest.mark.asyncio
def test_revoke_token_returns_204_when_successful(mock_revoke_token_use_case, mock_db):
    app.dependency_overrides = {
        JWTBearer: lambda: MockJWTBearer(),
        RevokeRefreshTokenService: lambda: mock_revoke_token_use_case,
        get_db: lambda: mock_db,
    }
    client = TestClient(app)
    refresh_token_payload = {
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImEwMGUxNTBlLTg5YWUtNDk4NS1hOTU5LTg5MmYyYWIxYzA5YSIsImV4cCI6MTczMzA1NDA0NX0.JCPClwQv7ocPdm-Lu1CJmlsAJVkIN_W0vN_68Db_Ssw"
    }

    response = client.post("/authentication:revoke", json=refresh_token_payload)

    assert response.status_code == 204

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from app.services.create_user_service import CreateUserService
from app.services.delete_user_by_id_service import DeleteUserByIdService
from app.services.get_all_users_service import GetAllUsersService
from app.services.get_user_by_id_service import GetUserByIdService
from app.services.update_user_service import UpdateUserService
from infra.persistence.adapters.db_connection import get_db
from main import app


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_create_user_use_case():
    mock = AsyncMock()
    mock.create.return_value = {
        "id": str(uuid4()),
        "name": "Test User",
        "email": "test@example.com",
    }
    return mock


@pytest.fixture
def mock_get_all_users_use_case():
    mock = AsyncMock()
    mock.get_all.return_value = [
        {"id": str(uuid4()), "name": "User 1", "email": "user1@example.com"},
        {"id": str(uuid4()), "name": "User 2", "email": "user2@example.com"},
    ]
    return mock


@pytest.fixture
def mock_get_user_by_id_use_case():
    mock = AsyncMock()
    mock.get_by_id.return_value = {
        "id": str(uuid4()),
        "name": "Test User",
        "email": "test@example.com",
    }
    return mock


@pytest.fixture
def mock_update_user_use_case():
    mock = AsyncMock()
    mock.update.return_value = {
        "id": str(uuid4()),
        "name": "Updated User",
        "email": "updated@example.com",
    }
    return mock


@pytest.fixture
def mock_delete_user_by_id_use_case():
    mock = AsyncMock()
    mock.delete_by_id.return_value = None
    return mock


def test_create_user_returns_201_when_successful(mock_create_user_use_case, mock_db):
    app.dependency_overrides = {
        CreateUserService: lambda: mock_create_user_use_case,
        get_db: lambda: mock_db,
    }
    client = TestClient(app)
    user_payload = {"name": "Test User", "email": "test@example.com"}

    response = client.post("/users", json=user_payload)

    assert response.status_code == 201
    assert response.json() == {
        "id": mock_create_user_use_case.create.return_value["id"],
        "name": "Test User",
        "email": "test@example.com",
    }


def test_get_all_users_returns_list_of_users(mock_get_all_users_use_case, mock_db):
    app.dependency_overrides = {
        GetAllUsersService: lambda: mock_get_all_users_use_case,
        get_db: lambda: mock_db,
    }
    client = TestClient(app)

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) == len(mock_get_all_users_use_case.get_all.return_value)
    assert response.json() == mock_get_all_users_use_case.get_all.return_value


def test_get_user_by_id_returns_user_when_id_exists(
    mock_get_user_by_id_use_case, mock_db
):
    app.dependency_overrides = {
        GetUserByIdService: lambda: mock_get_user_by_id_use_case,
        get_db: lambda: mock_db,
    }
    client = TestClient(app)
    test_user_id = str(uuid4())

    response = client.get(f"/users/{test_user_id}")

    assert response.status_code == 200
    assert response.json() == mock_get_user_by_id_use_case.get_by_id.return_value


def test_update_user_returns_updated_user_when_successful(
    mock_update_user_use_case, mock_db
):
    app.dependency_overrides = {
        UpdateUserService: lambda: mock_update_user_use_case,
        get_db: lambda: mock_db,
    }
    client = TestClient(app)
    test_user_id = str(uuid4())
    update_payload = {"name": "Updated User", "email": "updated@example.com"}

    response = client.put(f"/users/{test_user_id}", json=update_payload)

    assert response.status_code == 200
    assert response.json() == mock_update_user_use_case.update.return_value


def test_delete_user_by_id_returns_204_when_successful(
    mock_delete_user_by_id_use_case, mock_db
):
    app.dependency_overrides = {
        DeleteUserByIdService: lambda: mock_delete_user_by_id_use_case,
        get_db: lambda: mock_db,
    }
    client = TestClient(app)
    test_user_id = str(uuid4())

    response = client.delete(f"/users/{test_user_id}")

    assert response.status_code == 204

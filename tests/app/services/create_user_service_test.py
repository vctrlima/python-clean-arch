import pytest
from unittest.mock import MagicMock, AsyncMock
from app.services.create_user_service import CreateUserService
from domain.entities.user import User
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from infra.persistence.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4


@pytest.fixture
def mock_user_repository():
    mock = MagicMock(UserRepository)
    mock.create = AsyncMock(
        return_value={
            "id": str(uuid4()),
            "name": "Test User",
            "email": "test@example.com",
        }
    )
    return mock


@pytest.fixture
def mock_db():
    return MagicMock(AsyncSession)


@pytest.fixture
def create_user_service(mock_user_repository):
    return CreateUserService(repository=mock_user_repository)


@pytest.mark.asyncio
async def test_create_user(create_user_service, mock_user_repository, mock_db):
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password="securepassword",
    )

    response = await create_user_service.create(user, db=mock_db)

    mock_user_repository.create.assert_awaited_once_with(user, mock_db)
    assert isinstance(response, UserResponseDTO)
    assert response.id != None
    assert response.name == "Test User"
    assert response.email == "test@example.com"

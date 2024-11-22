from uuid import uuid4
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from app.services.update_user_service import UpdateUserService
from domain.entities.user import User
from infra.persistence.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user_repository():
    mock = MagicMock(UserRepository)
    mock.update = AsyncMock(
        return_value=User(
            id=str(uuid4()),
            name="Test User",
            email="test@example.com",
            password="securepassword",
        )
    )
    return mock


@pytest.fixture
def mock_db():
    return MagicMock(AsyncSession)


@pytest.fixture
def update_user_service(mock_user_repository):
    return UpdateUserService(repository=mock_user_repository)


@pytest.mark.asyncio
async def test_update_user(update_user_service, mock_user_repository, mock_db):
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password="securepassword",
    )

    response = await update_user_service.update(user, mock_db)

    mock_user_repository.update.assert_awaited_once_with(user, mock_db)
    assert isinstance(response, UserResponseDTO)
    assert response.id != None
    assert response.name == "Test User"
    assert response.email == "test@example.com"

import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from app.services.get_user_by_id_service import GetUserByIdService
from domain.entities.user import User
from infra.persistence.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user_repository():
    mock = MagicMock(UserRepository)
    mock.get_by_id = AsyncMock(
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
def get_user_by_id_service(mock_user_repository):
    return GetUserByIdService(repository=mock_user_repository)


@pytest.mark.asyncio
async def test_get_user_by_id(get_user_by_id_service, mock_user_repository, mock_db):
    user_id = str(uuid4())

    response = await get_user_by_id_service.get_by_id(user_id, mock_db)

    mock_user_repository.get_by_id.assert_awaited_once_with(user_id, mock_db)
    assert isinstance(response, UserResponseDTO)
    assert response.id != None
    assert response.name == "Test User"
    assert response.email == "test@example.com"

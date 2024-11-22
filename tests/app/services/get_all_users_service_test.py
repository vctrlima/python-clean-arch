from uuid import uuid4
import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from app.services.get_all_users_service import GetAllUsersService
from domain.entities.user import User
from domain.models.pageable_model import Pageable
from infra.persistence.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user_repository():
    mock = MagicMock(UserRepository)
    mock_content = []
    mock_user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password="securepassword",
    )
    mock_content.append(mock_user)
    pageable_mock = Pageable.create(
        mock_content, 10, 0, len(mock_content), len(mock_content)
    )
    mock.get_all = AsyncMock(return_value=pageable_mock)
    return mock


@pytest.fixture
def mock_db():
    return MagicMock(AsyncSession)


@pytest.fixture
def get_all_users_service(mock_user_repository):
    return GetAllUsersService(repository=mock_user_repository)


@pytest.mark.asyncio
async def test_get_all_users(get_all_users_service, mock_user_repository, mock_db):
    offset = 0
    limit = 10
    sort = "+name"

    response = await get_all_users_service.get_all(offset, limit, sort, mock_db)

    mock_user_repository.get_all.assert_awaited_once_with(offset, limit, sort, mock_db)
    assert len(response.content) == 1
    assert response.limit == limit
    assert response.offset == offset
    assert response.page_number == 1
    assert response.page_elements == 1
    assert response.total_pages == 1
    assert response.total_elements == 1

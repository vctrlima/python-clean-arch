import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.delete_user_by_id_service import DeleteUserByIdService
from infra.persistence.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user_repository():
    mock = MagicMock(UserRepository)
    mock.delete_by_id = AsyncMock(return_value={None})
    return mock


@pytest.fixture
def mock_db():
    return MagicMock(AsyncSession)


@pytest.fixture
def delete_user_by_id_service(mock_user_repository):
    return DeleteUserByIdService(repository=mock_user_repository)


@pytest.mark.asyncio
async def test_delete_user_by_id(
    delete_user_by_id_service, mock_user_repository, mock_db
):
    user_id = str(uuid4())

    await delete_user_by_id_service.delete_by_id(user_id, db=mock_db)

    mock_user_repository.delete_by_id.assert_awaited_once_with(user_id, mock_db)

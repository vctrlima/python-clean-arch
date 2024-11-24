import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.user import User
from domain.models.pageable_model import Pageable
from infra.persistence.models.user_model import UserModel
from infra.encryption.password_encryption import PasswordEncryption
from infra.persistence.repositories.user_repository import UserRepository


@pytest.fixture
def user_repository():
    return UserRepository()


@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def sample_user():
    return User(
        id=uuid4(),
        name="Test User",
        email="test@example.com",
        password="securepassword",
    )


@pytest.fixture
def sample_user_model(sample_user):
    return UserModel(
        user=sample_user,
        hashed_password=PasswordEncryption.encrypt(password=sample_user.password),
    )


@pytest.mark.asyncio
async def test_create_user(user_repository, mock_db, sample_user):
    with patch.object(PasswordEncryption, "encrypt", return_value="encryptedpassword"):
        mock_db.add = AsyncMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.refresh.side_effect = lambda user: setattr(user, "id", sample_user.id)

        result = await user_repository.create(sample_user, mock_db)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert result.id == sample_user.id
        assert result.name == sample_user.name
        assert result.email == sample_user.email
        assert result.password is None


@pytest.mark.asyncio
async def test_get_user_by_id(user_repository, mock_db, sample_user_model):
    mock_db.get = AsyncMock(return_value=sample_user_model)

    result = await user_repository.get_by_id(sample_user_model.id, mock_db)

    mock_db.get.assert_called_once_with(UserModel, sample_user_model.id)
    assert result.id == sample_user_model.id
    assert result.name == sample_user_model.name
    assert result.email == sample_user_model.email


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(user_repository, mock_db):
    mock_execute_result = AsyncMock()
    mock_execute_result.scalar_one_or_none.return_value = None
    mock_db.execute = AsyncMock(return_value=mock_execute_result)

    result = await user_repository.get_by_email("notfound@example.com", mock_db)

    assert result is None


@pytest.mark.asyncio
async def test_update_user(user_repository, mock_db, sample_user, sample_user_model):
    mock_db.get = AsyncMock(return_value=sample_user_model)
    mock_db.commit = AsyncMock()

    with patch.object(PasswordEncryption, "encrypt", return_value="updatedpassword"):
        updated_user = sample_user
        updated_user.name = "Updated Name"
        updated_user.email = "updated@example.com"
        result = await user_repository.update(updated_user, mock_db)

        mock_db.get.assert_called_once_with(UserModel, updated_user.id)
        mock_db.commit.assert_called_once()
        assert result.name == "Updated Name"
        assert result.email == "updated@example.com"


@pytest.mark.asyncio
async def test_delete_user_by_id(user_repository, mock_db, sample_user_model):
    mock_db.get = AsyncMock(return_value=sample_user_model)
    mock_db.delete = AsyncMock()
    mock_db.commit = AsyncMock()

    await user_repository.delete_by_id(sample_user_model.id, mock_db)

    mock_db.get.assert_called_once_with(UserModel, sample_user_model.id)
    mock_db.delete.assert_called_once_with(sample_user_model)
    mock_db.commit.assert_called_once()

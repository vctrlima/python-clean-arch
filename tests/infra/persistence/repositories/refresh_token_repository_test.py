import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from infra.persistence.models.refresh_token_model import RefreshTokenModel
from infra.persistence.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)


@pytest.fixture
def refresh_token_repository():
    return RefreshTokenRepository()


@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def sample_refresh_token():
    return RefreshTokenModel(
        hashed_token="hashed_token_example",
        user_id=uuid4(),
    )


@pytest.mark.asyncio
async def test_save_new_refresh_token(
    refresh_token_repository, mock_db, sample_refresh_token
):
    mock_db.execute = AsyncMock(
        return_value=AsyncMock(scalar_one_or_none=AsyncMock(return_value=None))
    )
    mock_db.add = AsyncMock()
    mock_db.commit = AsyncMock()
    refresh_token_repository.get_by_user_id = AsyncMock(return_value=None)

    await refresh_token_repository.save(sample_refresh_token, mock_db)

    mock_db.add.assert_called_once_with(sample_refresh_token)
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_save_existing_refresh_token(
    refresh_token_repository, mock_db, sample_refresh_token
):
    existing_token = RefreshTokenModel(
        hashed_token="hashed_token_old",
        user_id=sample_refresh_token.user_id,
    )
    refresh_token_repository.get_by_user_id = AsyncMock(return_value=existing_token)
    mock_db.commit = AsyncMock()

    await refresh_token_repository.save(sample_refresh_token, mock_db)

    mock_db.commit.assert_called_once()


import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from infra.persistence.models.refresh_token_model import RefreshTokenModel
from infra.persistence.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)


@pytest.mark.asyncio
async def test_get_by_hashed_token():
    hashed_token = "test_hashed_token"
    mock_refresh_token = RefreshTokenModel(
        hashed_token=hashed_token, user_id="123e4567-e89b-12d3-a456-426614174000"
    )
    mock_session = AsyncMock(spec=AsyncSession)
    mock_execute_result = MagicMock()
    mock_execute_result.scalar_one_or_none.return_value = mock_refresh_token
    mock_session.execute.return_value = mock_execute_result
    repository = RefreshTokenRepository()

    result = await repository.get_by_hashed_token(hashed_token, mock_session)

    assert result == mock_refresh_token
    mock_session.execute.assert_called_once()
    statement = mock_session.execute.call_args[0][0]
    assert str(statement).startswith("SELECT")
    assert "refresh_tokens" in str(statement)
    assert "hashed_token = :hashed_token" in str(statement)


@pytest.mark.asyncio
async def test_get_by_user_id():
    user_id = uuid4()
    hashed_token = "test_hashed_token"
    mock_refresh_token = RefreshTokenModel(hashed_token=hashed_token, user_id=user_id)
    mock_session = AsyncMock(spec=AsyncSession)
    mock_execute_result = MagicMock()
    mock_execute_result.scalar_one_or_none.return_value = mock_refresh_token
    mock_session.execute.return_value = mock_execute_result
    repository = RefreshTokenRepository()

    result = await repository.get_by_user_id(user_id, mock_session)

    assert result == mock_refresh_token
    mock_session.execute.assert_called_once()
    statement = mock_session.execute.call_args[0][0]
    assert str(statement).startswith("SELECT")


@pytest.mark.asyncio
async def test_delete_by_user_id(
    refresh_token_repository, mock_db, sample_refresh_token
):
    mock_db.execute = AsyncMock()
    mock_db.commit = AsyncMock()

    await refresh_token_repository.delete_by_user_id(
        sample_refresh_token.user_id, mock_db
    )

    mock_db.commit.assert_called_once()

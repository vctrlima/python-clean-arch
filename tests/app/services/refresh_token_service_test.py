import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.refresh_token_service import RefreshTokenService
from app.data_transfer_objects.authentication_response_dto import (
    AuthenticationResponseDTO,
)
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from infra.persistence.models.refresh_token_model import RefreshTokenModel


@pytest.fixture
def mock_refresh_token_model():
    return RefreshTokenModel(
        hashed_token="mock_refresh_token",
        user_id=uuid4(),
    )


@pytest.fixture
def mock_user_dto():
    return UserResponseDTO(
        id=uuid4(),
        name="Jane Doe",
        email="jane.doe@example.com",
    )


@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_user_repository(mock_user_dto):
    user_repository = AsyncMock()
    user_repository.get_by_id.return_value = mock_user_dto
    return user_repository


@pytest.fixture
def mock_refresh_token_repository(mock_refresh_token_model):
    refresh_token_repository = AsyncMock()
    refresh_token_repository.get_by_hashed_token.return_value = mock_refresh_token_model
    refresh_token_repository.save.return_value = None
    return refresh_token_repository


@pytest.fixture
def service(mock_user_repository, mock_refresh_token_repository):
    return RefreshTokenService(
        user_repository=mock_user_repository,
        refresh_token_repository=mock_refresh_token_repository,
    )


@patch("app.services.refresh_token_service.TokenAuthorization.decode")
@patch("app.services.refresh_token_service.TokenAuthorization.generate_access_token")
@patch("app.services.refresh_token_service.TokenAuthorization.generate_refresh_token")
@pytest.mark.asyncio
async def test_refresh_success(
    mock_generate_refresh_token,
    mock_generate_access_token,
    mock_decode,
    service,
    mock_user_dto,
    mock_db_session,
):
    mock_decode.return_value = {
        "id": str(mock_user_dto.id),
        "exp": (datetime.now(timezone.utc) + timedelta(days=1)).timestamp(),
    }
    mock_generate_access_token.return_value = "new_access_token"
    mock_generate_refresh_token.return_value = "new_refresh_token"

    result = await service.refresh("mock_refresh_token", mock_db_session)

    assert isinstance(result, AuthenticationResponseDTO)
    assert result.user == mock_user_dto
    assert result.credentials.access_token == "new_access_token"
    assert result.credentials.refresh_token == "new_refresh_token"
    service.refresh_token_repository.get_by_hashed_token.assert_awaited_once_with(
        "mock_refresh_token", mock_db_session
    )
    service.refresh_token_repository.save.assert_awaited_once()
    service.user_repository.get_by_id.assert_awaited_once_with(
        mock_user_dto.id, mock_db_session
    )


@patch("app.services.refresh_token_service.TokenAuthorization.decode")
@pytest.mark.asyncio
async def test_refresh_invalid_token(mock_decode, service, mock_db_session):
    service.refresh_token_repository.get_by_hashed_token.return_value = None

    with pytest.raises(Exception, match="Invalid refresh token hash"):
        await service.refresh("invalid_token", mock_db_session)

    service.refresh_token_repository.get_by_hashed_token.assert_awaited_once_with(
        "invalid_token", mock_db_session
    )
    mock_decode.assert_not_called()


@patch("app.services.refresh_token_service.TokenAuthorization.decode")
@pytest.mark.asyncio
async def test_refresh_token_expired(mock_decode, service, mock_db_session):
    mock_decode.return_value = {
        "id": str(uuid4()),
        "exp": (datetime.now(timezone.utc) - timedelta(seconds=1)).timestamp(),
    }

    with pytest.raises(Exception, match="Refresh token expired"):
        await service.refresh("mock_refresh_token", mock_db_session)

    service.refresh_token_repository.get_by_hashed_token.assert_awaited_once_with(
        "mock_refresh_token", mock_db_session
    )


@patch("app.services.refresh_token_service.TokenAuthorization.decode")
@pytest.mark.asyncio
async def test_refresh_user_not_found(mock_decode, service, mock_db_session):
    mock_decode.return_value = {
        "id": str(uuid4()),
        "exp": (datetime.now(timezone.utc) + timedelta(days=1)).timestamp(),
    }
    service.user_repository.get_by_id.return_value = None

    with pytest.raises(Exception, match="Invalid user read from refresh token"):
        await service.refresh("mock_refresh_token", mock_db_session)

    service.refresh_token_repository.get_by_hashed_token.assert_awaited_once_with(
        "mock_refresh_token", mock_db_session
    )
    service.user_repository.get_by_id.assert_awaited_once()

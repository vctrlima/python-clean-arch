import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from app.services.authenticate_user_service import AuthenticateUserService
from app.data_transfer_objects.authentication_response_dto import (
    AuthenticationResponseDTO,
)
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from domain.entities.user import User
from infra.persistence.models.refresh_token_model import RefreshTokenModel


@pytest.fixture
def mock_user():
    return User(
        id=uuid4(),
        name="John Doe",
        email="john.doe@example.com",
        password="hashed_password",
    )


@pytest.fixture
def mock_refresh_token():
    return RefreshTokenModel(
        user_id=uuid4(),
        hashed_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImEwMGUxNTBlLTg5YWUtNDk4NS1hOTU5LTg5MmYyYWIxYzA5YSIsImV4cCI6MTczMzA1NDA0NX0.JCPClwQv7ocPdm-Lu1CJmlsAJVkIN_W0vN_68Db_Ssw",
    )


@pytest.fixture
def mock_user_dto(mock_user):
    return UserResponseDTO(
        id=mock_user.id,
        name=mock_user.name,
        email=mock_user.email,
    )


@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_user_repository(mock_user):
    user_repository = AsyncMock()
    user_repository.get_by_email.return_value = mock_user
    return user_repository


@pytest.fixture
def mock_refresh_token_repository(mock_refresh_token):
    refresh_token_repository = AsyncMock()
    refresh_token_repository.save.return_value = mock_refresh_token
    return refresh_token_repository


@pytest.fixture
def service(mock_user_repository, mock_refresh_token_repository):
    return AuthenticateUserService(
        user_repository=mock_user_repository,
        refresh_token_repository=mock_refresh_token_repository,
    )


@patch("app.services.authenticate_user_service.PasswordEncryption.verify")
@patch("app.services.authenticate_user_service.TokenAuthorization.encode")
@pytest.mark.asyncio
async def test_authenticate_success(
    mock_encode, mock_verify, service, mock_user, mock_user_dto, mock_db_session
):
    mock_verify.return_value = True
    mock_encode.return_value = "mock_token"

    result = await service.authenticate(mock_user.email, "password", mock_db_session)

    assert isinstance(result, AuthenticationResponseDTO)
    assert result.user == mock_user_dto
    assert result.credentials.access_token == "mock_token"
    service.user_repository.get_by_email.assert_awaited_once_with(
        mock_user.email, mock_db_session
    )
    service.refresh_token_repository.save.assert_awaited_once()
    mock_verify.assert_called_once_with("password", hash=mock_user.password)


@patch("app.services.authenticate_user_service.PasswordEncryption.verify")
@pytest.mark.asyncio
async def test_authenticate_invalid_password(
    mock_verify, service, mock_user, mock_db_session
):
    mock_verify.return_value = False

    with pytest.raises(Exception, match="Invalid password"):
        await service.authenticate(mock_user.email, "wrong_password", mock_db_session)

    service.user_repository.get_by_email.assert_awaited_once_with(
        mock_user.email, mock_db_session
    )
    mock_verify.assert_called_once_with("wrong_password", hash=mock_user.password)


@pytest.mark.asyncio
async def test_authenticate_user_not_found(service, mock_db_session):
    service.user_repository.get_by_email.return_value = None

    with pytest.raises(Exception, match="User not found"):
        await service.authenticate(
            "nonexistent@example.com", "password", mock_db_session
        )

    service.user_repository.get_by_email.assert_awaited_once_with(
        "nonexistent@example.com", mock_db_session
    )

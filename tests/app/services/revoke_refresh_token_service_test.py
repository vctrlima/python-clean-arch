import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.revoke_refresh_token_service import RevokeRefreshTokenService
from infra.persistence.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from infra.authorization.token_authorization import TokenAuthorization
import uuid


@pytest.mark.asyncio
async def test_revoke_refresh_token_success():
    mock_refresh_token_repository = AsyncMock(spec=RefreshTokenRepository)
    mock_db_session = MagicMock()
    mock_token = "mock_refresh_token"
    mock_decoded_token = {"id": str(uuid.uuid4())}
    TokenAuthorization.decode = MagicMock(return_value=mock_decoded_token)
    service = RevokeRefreshTokenService(
        refresh_token_repository=mock_refresh_token_repository
    )

    await service.revoke(refresh_token=mock_token, db=mock_db_session)

    TokenAuthorization.decode.assert_called_once_with(mock_token)
    mock_refresh_token_repository.delete_by_user_id.assert_called_once_with(
        user_id=uuid.UUID(mock_decoded_token["id"]),
        db=mock_db_session,
    )


@pytest.mark.asyncio
async def test_revoke_refresh_token_invalid_token():
    mock_refresh_token_repository = AsyncMock(spec=RefreshTokenRepository)
    mock_db_session = MagicMock()
    mock_token = "invalid_refresh_token"
    TokenAuthorization.decode = MagicMock(side_effect=Exception("Invalid token"))

    service = RevokeRefreshTokenService(
        refresh_token_repository=mock_refresh_token_repository
    )

    with pytest.raises(Exception, match="Invalid token"):
        await service.revoke(refresh_token=mock_token, db=mock_db_session)
    TokenAuthorization.decode.assert_called_once_with(mock_token)
    mock_refresh_token_repository.delete_by_user_id.assert_not_called()

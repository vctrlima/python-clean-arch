import uuid
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from domain.use_cases.revoke_refresh_token import RevokeRefreshToken
from infra.authorization.token_authorization import TokenAuthorization
from infra.persistence.adapters.db_connection import get_db
from infra.persistence.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)


class RevokeRefreshTokenService(RevokeRefreshToken):
    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepository = Depends(
            RefreshTokenRepository
        ),
    ):
        self.refresh_token_repository = refresh_token_repository

    async def revoke(
        self, refresh_token: str, db: AsyncSession = Depends(get_db)
    ) -> None:
        decoded_token = TokenAuthorization.decode(refresh_token)
        user_id = uuid.UUID(str(decoded_token["id"]))
        await self.refresh_token_repository.delete_by_user_id(user_id=user_id, db=db)

import uuid
from fastapi import Depends
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from domain.models.credentials_model import Credentials
from domain.use_cases.refresh_token import RefreshToken
from app.data_transfer_objects.authentication_response_dto import (
    AuthenticationResponseDTO,
)
from infra.authorization.token_authorization import TokenAuthorization
from infra.persistence.adapters.db_connection import get_db
from infra.persistence.models.refresh_token_model import RefreshTokenModel
from infra.persistence.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from infra.persistence.repositories.user_repository import UserRepository


class RefreshTokenService(RefreshToken):
    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository),
        refresh_token_repository: RefreshTokenRepository = Depends(
            RefreshTokenRepository
        ),
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    async def refresh(
        self, refresh_token: str, db: AsyncSession = Depends(get_db)
    ) -> AuthenticationResponseDTO:
        saved_refresh_token = await self.refresh_token_repository.get_by_hashed_token(
            refresh_token, db
        )
        if not saved_refresh_token:
            raise Exception("Invalid refresh token hash")
        decoded_token = TokenAuthorization.decode(saved_refresh_token.hashed_token)
        if datetime.now(timezone.utc).timestamp() > decoded_token["exp"]:
            raise Exception("Refresh token expired")
        user_id = uuid.UUID(str(decoded_token["id"]))
        user = await self.user_repository.get_by_id(user_id, db)
        if not user:
            raise Exception("Invalid user read from refresh token")
        user_dto = UserResponseDTO.model_validate(user)
        access_token = TokenAuthorization.generate_access_token(user_dto=user_dto)
        refresh_token = TokenAuthorization.generate_refresh_token(user_dto=user_dto)
        refresh_token_model = RefreshTokenModel(
            hashed_token=refresh_token, user_id=user_dto.id
        )
        await self.refresh_token_repository.save(
            refresh_token=refresh_token_model, db=db
        )
        credentials = Credentials.create(
            access_token=access_token, refresh_token=refresh_token
        )
        return AuthenticationResponseDTO(user=user_dto, credentials=credentials)

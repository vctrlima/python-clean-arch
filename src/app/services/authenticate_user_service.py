from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_transfer_objects.authentication_response_dto import (
    AuthenticationResponseDTO,
)
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from domain.models.credentials_model import Credentials
from domain.use_cases.authenticate_user import AuthenticateUser
from infra.authorization.token_authorization import TokenAuthorization
from infra.encryption.password_encryption import PasswordEncryption
from infra.persistence.adapters.db_connection import get_db
from infra.persistence.models.refresh_token_model import RefreshTokenModel
from infra.persistence.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from infra.persistence.repositories.user_repository import UserRepository


class AuthenticateUserService(AuthenticateUser):
    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository),
        refresh_token_repository: RefreshTokenRepository = Depends(
            RefreshTokenRepository
        ),
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    async def authenticate(
        self, email: str, password: str, db: AsyncSession = Depends(get_db)
    ) -> AuthenticationResponseDTO:
        user = await self.user_repository.get_by_email(email, db)
        if not user:
            raise Exception("User not found")
        password_is_valid = PasswordEncryption.verify(password, hash=user.password)
        if not password_is_valid:
            raise Exception("Invalid password")
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

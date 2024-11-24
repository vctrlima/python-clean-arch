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
from infra.persistence.repositories.user_repository import UserRepository


class AuthenticateUserService(AuthenticateUser):
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    async def authenticate(
        self, email: str, password: str, db: AsyncSession = Depends(get_db)
    ) -> AuthenticationResponseDTO:
        try:
            user = await self.repository.get_by_email(email, db)
            if not user:
                raise Exception("User not found")
            password_is_valid = PasswordEncryption.verify(password, hash=user.password)
            if not password_is_valid:
                raise Exception("Invalid password")
            user_dto = UserResponseDTO.model_validate(user)
            payload = {
                "id": str(user_dto.id),
                "name": user_dto.name,
                "email": user_dto.email,
            }
            token = TokenAuthorization.encode(payload)
            credentials = Credentials.create(token=token)
            return AuthenticationResponseDTO(user=user_dto, credentials=credentials)
        except Exception as exception:
            print(exception)
            raise Exception(exception)

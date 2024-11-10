from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from domain.use_cases.create_user import CreateUser
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from domain.entities.user import User
from infra.persistence.adapters.db_connection import get_db
from infra.persistence.repositories.user_repository import UserRepository

class CreateUserService(CreateUser):
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    async def create(self, user: User, db: AsyncSession = Depends(get_db)) -> UserResponseDTO:
        return UserResponseDTO.model_validate(await self.repository.create(user, db))

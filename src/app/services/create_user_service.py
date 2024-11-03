from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.user import User
from src.infra.persistence.adapters.db_connection import get_db
from src.infra.persistence.repositories.user_repository import UserRepository

class CreateUserService:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    async def create(self, user: User, db: AsyncSession = Depends(get_db)) -> User:
        return await self.repository.create(user, db)

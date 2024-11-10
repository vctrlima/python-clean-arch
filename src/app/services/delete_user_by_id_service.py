from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infra.persistence.adapters.db_connection import get_db
from infra.persistence.repositories.user_repository import UserRepository


class DeleteUserByIdService:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    async def delete_by_id(self, id: UUID, db: AsyncSession = Depends(get_db)) -> None:
        return await self.repository.delete_by_id(id, db)

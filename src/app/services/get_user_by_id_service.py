from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from domain.use_cases.get_user_by_id import GetUserById
from infra.persistence.adapters.db_connection import get_db
from infra.persistence.repositories.user_repository import UserRepository


class GetUserByIdService(GetUserById):
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    async def get_by_id(
        self, id: UUID, db: AsyncSession = Depends(get_db)
    ) -> UserResponseDTO:
        return UserResponseDTO.model_validate(await self.repository.get_by_id(id, db))

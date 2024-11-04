from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.data_transfer_objects.user_response_dto import UserResponseDTO
from src.app.data_transfer_objects.pageable_dto import Pageable
from src.infra.persistence.adapters.db_connection import get_db
from src.infra.persistence.repositories.user_repository import UserRepository

class GetUsersService:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    async def get(
        self,
        _offset: int = 0,
        _limit: int = 10,
        _sort: str = "+name",
        db: AsyncSession = Depends(get_db)
    ) -> Pageable[UserResponseDTO]:
        found_users = await self.repository.get(_offset, _limit, _sort, db)
        list_of_users = []
        for user in found_users:
            list_of_users.append(UserResponseDTO.model_validate(user))
        return Pageable[UserResponseDTO](content=list_of_users)

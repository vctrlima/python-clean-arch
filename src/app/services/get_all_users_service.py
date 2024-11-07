from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.data_transfer_objects.user_response_dto import UserResponseDTO
from src.domain.models.pageable_model import Pageable
from src.domain.use_cases.get_all_users import GetAllUsers
from src.infra.persistence.adapters.db_connection import get_db
from src.infra.persistence.repositories.user_repository import UserRepository

class GetAllUsersService(GetAllUsers):
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 10,
        sort: str = "+name",
        db: AsyncSession = Depends(get_db)
    ) -> Pageable[UserResponseDTO]:
        found_users = await self.repository.get_all(offset, limit, sort, db)
        mapped_users = []
        [mapped_users.append(UserResponseDTO.model_validate(user)) for user in found_users.content]
        return Pageable.create(mapped_users, limit, offset, found_users.total_elements, len(mapped_users))

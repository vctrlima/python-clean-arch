from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.data_transfer_objects.user_response_dto import UserResponseDTO
from src.domain.models.pageable_model import Pageable
from src.domain.use_cases.get_users import GetUsers
from src.infra.persistence.adapters.db_connection import get_db
from src.infra.persistence.repositories.user_repository import UserRepository

class GetUsersService(GetUsers):
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    async def get(
        self,
        offset: int = 0,
        limit: int = 10,
        _sort: str = "+name",
        db: AsyncSession = Depends(get_db)
    ) -> Pageable[UserResponseDTO]:
        found_users = await self.repository.get(offset, limit, _sort, db)
        mapped_users = []
        [mapped_users.append(UserResponseDTO.model_validate(user)) for user in found_users.content]
        return Pageable.create(mapped_users, limit, offset, found_users.total_elements, len(mapped_users))

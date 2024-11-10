from abc import abstractmethod
from uuid import UUID
from domain.entities.user import User

class GetUserById:
    @abstractmethod
    async def get_by_id(self, id: UUID) -> User:
        pass

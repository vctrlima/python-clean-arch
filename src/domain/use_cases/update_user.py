from abc import abstractmethod
from domain.entities.user import User


class UpdateUser:
    @abstractmethod
    async def update(self, user: User) -> User:
        pass

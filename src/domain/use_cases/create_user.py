from abc import abstractmethod
from domain.entities.user import User


class CreateUser:
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

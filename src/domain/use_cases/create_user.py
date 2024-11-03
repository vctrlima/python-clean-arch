from abc import abstractmethod
from src.domain.entities.user import User

class CreateUser:
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

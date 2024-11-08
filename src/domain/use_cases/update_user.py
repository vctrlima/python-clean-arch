from abc import abstractmethod
from src.domain.entities.user import User

class UpdateUser:
    @abstractmethod
    async def update(self, user: User) -> User:
        pass

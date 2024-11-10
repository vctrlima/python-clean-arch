from abc import abstractmethod
from typing import List

from domain.entities.user import User


class GetAllUsers:
    @abstractmethod
    async def get_all(
        self, offset: int = 0, limit: int = 10, _sort: str = "+name"
    ) -> List[User]:
        pass

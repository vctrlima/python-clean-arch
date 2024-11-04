from abc import abstractmethod
from typing import List

from src.domain.entities.user import User

class GetUsers:
    @abstractmethod
    async def get(self, _offset: int = 0, _limit: int = 10, _sort: str = "+name") -> List[User]:
        pass
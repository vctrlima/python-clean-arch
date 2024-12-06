from abc import abstractmethod
from domain.entities.user import User
from domain.models.pageable_model import Pageable


class GetAllUsers:
    @abstractmethod
    async def get_all(
        self, offset: int = 0, limit: int = 10, _sort: str = "+name"
    ) -> Pageable[User]:
        pass

from abc import abstractmethod
from uuid import UUID

class DeleteUserById:
    @abstractmethod
    async def delete_by_id(self, id: UUID) -> None:
        pass

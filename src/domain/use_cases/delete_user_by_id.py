from abc import abstractmethod
from uuid import UUID

class DeleteUserById:
    @abstractmethod
    async def delete_by_id(id: UUID) -> None:
        pass

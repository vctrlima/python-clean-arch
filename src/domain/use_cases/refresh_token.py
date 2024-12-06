from abc import abstractmethod
from domain.models.authentication_model import Authentication


class RefreshToken:
    @abstractmethod
    async def refresh(self, refresh_token: str) -> Authentication:
        pass

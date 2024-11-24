from abc import abstractmethod
from domain.models.authentication_model import Authentication


class AuthenticateUser:
    @abstractmethod
    async def authenticate(self, email: str, password: str) -> Authentication:
        pass

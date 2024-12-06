from abc import abstractmethod


class RevokeRefreshToken:
    @abstractmethod
    async def revoke(self, refresh_token: str) -> None:
        pass

from datetime import datetime
from pydantic import BaseModel, Field


class Credentials(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")
    timestamp: datetime = Field(..., alias="timestamp")

    @classmethod
    def create(cls, access_token: str, refresh_token=refresh_token):
        return cls(
            accessToken=access_token,
            refreshToken=refresh_token,
            timestamp=datetime.now(),
        )

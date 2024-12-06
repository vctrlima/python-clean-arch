from pydantic import BaseModel, ConfigDict, Field


class RefreshTokenRequestDTO(BaseModel):
    refresh_token: str = Field(..., alias="refreshToken")

    model_config = ConfigDict(from_attributes=True)

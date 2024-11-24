from pydantic import BaseModel, ConfigDict


class AuthenticationRequestDTO(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)

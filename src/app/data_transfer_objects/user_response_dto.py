from uuid import UUID
from pydantic import BaseModel, ConfigDict


class UserResponseDTO(BaseModel):
    id: UUID = None
    name: str = ""
    email: str = ""

    model_config = ConfigDict(from_attributes=True)

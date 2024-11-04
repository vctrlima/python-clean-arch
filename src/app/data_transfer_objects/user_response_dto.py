from uuid import UUID
from pydantic import BaseModel, ConfigDict
from src.domain.entities.user import User

class UserResponseDTO(BaseModel):
    id: UUID = None
    name: str = ""
    email: str = ""

    model_config = ConfigDict(from_attributes=True)

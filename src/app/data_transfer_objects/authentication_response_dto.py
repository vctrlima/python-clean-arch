from pydantic import BaseModel, ConfigDict
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from domain.models.credentials_model import Credentials


class AuthenticationResponseDTO(BaseModel):
    user: UserResponseDTO
    credentials: Credentials

    model_config = ConfigDict(from_attributes=True)

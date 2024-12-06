from uuid import uuid4
import pytest
from datetime import datetime

from app.data_transfer_objects.authentication_response_dto import (
    AuthenticationResponseDTO,
)
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from domain.models.credentials_model import Credentials


def test_authentication_response_dto_custom_values():
    user_dto = UserResponseDTO(
        id=uuid4(), name="John Doe", email="john.doe@example.com"
    )
    credentials = Credentials(
        timestamp=datetime.now(),
        accessToken="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImEwMGUxNTBlLTg5YWUtNDk4NS1hOTU5LTg5MmYyYWIxYzA5YSIsIm5hbWUiOiJWaWN0b3IgQ2FyZG9zbyBMaW1hIiwiZW1haWwiOiJ2aWN0b3IubGltYUBlbWFpbCJ9.-4q1O2tyFfyXMvDQ2ompdmYohQlgYkU5T9blsQmkjhk",
        refreshToken="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImEwMGUxNTBlLTg5YWUtNDk4NS1hOTU5LTg5MmYyYWIxYzA5YSIsImV4cCI6MTczMzA1NDA0NX0.JCPClwQv7ocPdm-Lu1CJmlsAJVkIN_W0vN_68Db_Ssw",
    )

    authentication_response_dto = AuthenticationResponseDTO(
        user=user_dto, credentials=credentials
    )

    assert authentication_response_dto.user == user_dto
    assert authentication_response_dto.credentials == credentials

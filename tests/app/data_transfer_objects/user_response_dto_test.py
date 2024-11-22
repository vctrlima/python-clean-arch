import pytest
from uuid import UUID, uuid4
from app.data_transfer_objects.user_response_dto import UserResponseDTO


def test_user_response_dto_default_values():
    user_dto = UserResponseDTO()

    assert user_dto.id is None
    assert user_dto.name == ""
    assert user_dto.email == ""


def test_user_response_dto_custom_values():
    user_dto = UserResponseDTO(
        id=uuid4(), name="John Doe", email="john.doe@example.com"
    )

    assert isinstance(user_dto.id, UUID)
    assert user_dto.name == "John Doe"
    assert user_dto.email == "john.doe@example.com"


def test_user_response_dto_invalid_id():
    with pytest.raises(ValueError):
        UserResponseDTO(id="invalid-id", name="John Doe", email="john.doe@example.com")


def test_user_response_dto_from_attributes():
    user_dict = {"id": uuid4(), "name": "Jane Doe", "email": "jane.doe@example.com"}
    user_dto = UserResponseDTO.model_validate(user_dict)

    assert isinstance(user_dto.id, UUID)
    assert user_dto.name == "Jane Doe"
    assert user_dto.email == "jane.doe@example.com"

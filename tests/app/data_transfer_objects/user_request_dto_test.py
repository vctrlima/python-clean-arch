import pytest
from domain.entities.user import User
from app.data_transfer_objects.user_request_dto import UserRequestDTO


def test_user_request_dto_default_values():
    user_dto = UserRequestDTO()

    assert user_dto.id == ""
    assert user_dto.name == ""
    assert user_dto.email == ""
    assert user_dto.password == ""


def test_user_request_dto_custom_values():
    user_dto = UserRequestDTO(
        id="123",
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword",
    )

    assert user_dto.id == "123"
    assert user_dto.name == "John Doe"
    assert user_dto.email == "john.doe@example.com"
    assert user_dto.password == "securepassword"


def test_to_entity():
    user_dto = UserRequestDTO(
        id="123",
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword",
    )

    user_entity = user_dto.to_entity()

    assert isinstance(user_entity, User)
    assert user_entity.id == "123"
    assert user_entity.name == "John Doe"
    assert user_entity.email == "john.doe@example.com"
    assert user_entity.password == "securepassword"


def test_user_request_dto_optional_id():
    user_dto = UserRequestDTO(
        name="John Doe", email="john.doe@example.com", password="securepassword"
    )

    assert user_dto.id == ""

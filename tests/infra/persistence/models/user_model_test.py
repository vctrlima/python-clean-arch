import pytest
from uuid import uuid4
from domain.entities.user import User
from infra.encryption.password_encryption import PasswordEncryption
from infra.persistence.models.user_model import UserModel


def test_user_model_with_values():
    user_entity = User(
        id=uuid4(),
        name="Test User",
        email="test@example.com",
        password="securepassword",
    )
    user_hashed_password = PasswordEncryption.encrypt(user_entity.password)

    user_model = UserModel(user=user_entity, hashed_password=user_hashed_password)

    assert user_model.id != None
    assert user_model.name == user_entity.name
    assert user_model.email == user_entity.email
    assert user_model.password == user_hashed_password

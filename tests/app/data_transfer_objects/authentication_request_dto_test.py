import pytest
from app.data_transfer_objects.authentication_request_dto import (
    AuthenticationRequestDTO,
)


def test_authentication_request_dto_custom_values():
    authentication_request_dto = AuthenticationRequestDTO(
        email="john.doe@example.com", password="securepassword"
    )

    assert authentication_request_dto.email == "john.doe@example.com"
    assert authentication_request_dto.password == "securepassword"

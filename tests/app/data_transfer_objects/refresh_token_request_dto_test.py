from app.data_transfer_objects.refresh_token_request_dto import RefreshTokenRequestDTO
import pytest


def test_refresh_token_request_dto_creation():
    data = {"refreshToken": "test_refresh_token_value"}

    dto = RefreshTokenRequestDTO(**data)

    assert dto.refresh_token == data["refreshToken"]


def test_refresh_token_request_dto_alias():
    data = {"refreshToken": "test_refresh_token_value"}

    dto = RefreshTokenRequestDTO(**data)

    dto_dict = dto.dict(by_alias=True)
    assert dto_dict["refreshToken"] == data["refreshToken"]
    assert "refresh_token" not in dto_dict

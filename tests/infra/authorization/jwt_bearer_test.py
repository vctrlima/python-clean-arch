import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request
from infra.authorization.jwt_bearer import JWTBearer
from infra.authorization.token_authorization import TokenAuthorization


class MockRequest:
    def __init__(self, headers):
        self.headers = headers

    async def body(self):
        return b""


@pytest.fixture
def jwt_bearer():
    return JWTBearer()


@pytest.fixture
def valid_token(monkeypatch):
    def mock_verify(token: str):
        return {"id": "123", "name": "Test User", "email": "test@example.com"}

    monkeypatch.setattr(TokenAuthorization, "verify", mock_verify)
    return "valid_token"


@pytest.fixture
def invalid_token(monkeypatch):
    def mock_verify(token: str):
        raise HTTPException(status_code=403, detail="Invalid token or expired token")

    monkeypatch.setattr(TokenAuthorization, "verify", mock_verify)
    return "invalid_token"


@pytest.mark.asyncio
async def test_jwt_bearer_valid_token(jwt_bearer, valid_token):
    request = MockRequest(headers={"Authorization": f"Bearer {valid_token}"})
    token = await jwt_bearer.__call__(request)
    assert token == valid_token


@pytest.mark.asyncio
async def test_jwt_bearer_invalid_token(jwt_bearer, invalid_token):
    request = MockRequest(headers={"Authorization": f"Bearer {invalid_token}"})
    with pytest.raises(HTTPException) as exc_info:
        await jwt_bearer.__call__(request)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Invalid token or expired token"


def test_verify_jwt_valid_token(jwt_bearer, valid_token):
    assert jwt_bearer.verify_jwt(valid_token) is True


def test_verify_jwt_invalid_token(jwt_bearer, invalid_token):
    assert jwt_bearer.verify_jwt(invalid_token) is False

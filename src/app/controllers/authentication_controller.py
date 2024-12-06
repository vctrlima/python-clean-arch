from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_transfer_objects.authentication_request_dto import (
    AuthenticationRequestDTO,
)
from app.data_transfer_objects.authentication_response_dto import (
    AuthenticationResponseDTO,
)
from app.data_transfer_objects.refresh_token_request_dto import RefreshTokenRequestDTO
from app.services.authenticate_user_service import AuthenticateUserService
from app.services.refresh_token_service import RefreshTokenService
from app.services.revoke_refresh_token_service import RevokeRefreshTokenService
from domain.use_cases.authenticate_user import AuthenticateUser
from domain.use_cases.refresh_token import RefreshToken
from domain.use_cases.revoke_refresh_token import RevokeRefreshToken
from infra.authorization.jwt_bearer import JWTBearer
from infra.persistence.adapters.db_connection import get_db

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=AuthenticationResponseDTO,
)
async def authenticate(
    authentication_dto: AuthenticationRequestDTO = Body(...),
    authenticate_user_use_case: AuthenticateUser = Depends(AuthenticateUserService),
    db: AsyncSession = Depends(get_db),
):
    email = authentication_dto.email
    password = authentication_dto.password
    try:
        return await authenticate_user_use_case.authenticate(email, password, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials!")


@router.post(
    ":refresh",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_200_OK,
    response_model=AuthenticationResponseDTO,
)
async def refresh_token(
    refresh_token_dto: RefreshTokenRequestDTO = Body(...),
    refresh_token_use_case: RefreshToken = Depends(RefreshTokenService),
    db: AsyncSession = Depends(get_db),
):
    try:
        refresh_token = refresh_token_dto.refresh_token
        return await refresh_token_use_case.refresh(refresh_token, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token expired!")


@router.post(
    ":revoke",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def revoke_token(
    refresh_token_dto: RefreshTokenRequestDTO = Body(...),
    revoke_token_use_case: RevokeRefreshToken = Depends(RevokeRefreshTokenService),
    db: AsyncSession = Depends(get_db),
):
    try:
        refresh_token = refresh_token_dto.refresh_token
        await revoke_token_use_case.revoke(refresh_token, db)
    except Exception:
        raise HTTPException(status_code=401, detail="An error occurred on token revoke")

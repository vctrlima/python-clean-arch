from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_transfer_objects.authentication_request_dto import (
    AuthenticationRequestDTO,
)
from app.services.authenticate_user_service import AuthenticateUserService
from domain.use_cases.authenticate_user import AuthenticateUser
from infra.persistence.adapters.db_connection import get_db

router = APIRouter()


@router.post("/authenticate", status_code=status.HTTP_200_OK)
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

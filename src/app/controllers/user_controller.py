from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.data_transfer_objects.user_dto import UserDTO
from src.app.services.create_user_service import CreateUserService
from src.infra.persistence.adapters.db_connection import get_db

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_dto: UserDTO = Body(...),
    create_user_service: CreateUserService = Depends(CreateUserService),
    db: AsyncSession = Depends(get_db)
):
    user_entity = user_dto.to_entity()
    return await create_user_service.create(user_entity, db)

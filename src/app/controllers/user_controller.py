from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.use_cases.create_user import CreateUser
from src.domain.use_cases.get_users import GetUsers
from src.app.data_transfer_objects.user_request_dto import UserRequestDTO
from src.app.services.create_user_service import CreateUserService
from src.app.services.get_users_service import GetUsersService
from src.infra.persistence.adapters.db_connection import get_db

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_dto: UserRequestDTO = Body(...),
    create_user_use_case: CreateUser = Depends(CreateUserService),
    db: AsyncSession = Depends(get_db)
):
    user_entity = user_dto.to_entity()
    return await create_user_use_case.create(user_entity, db)

@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(
    offset: int = 0,
    limit: int = 10,
    sort: str = "+name",
    get_users_use_case: GetUsers = Depends(GetUsersService),
    db: AsyncSession = Depends(get_db)
):
    return await get_users_use_case.get(offset, limit, sort, db)
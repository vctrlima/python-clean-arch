from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.data_transfer_objects.pageable_dto import Pageable
from src.app.data_transfer_objects.user_request_dto import UserRequestDTO
from src.app.data_transfer_objects.user_response_dto import UserResponseDTO
from src.app.services.create_user_service import CreateUserService
from src.app.services.get_users_service import GetUsersService
from src.infra.persistence.adapters.db_connection import get_db

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponseDTO)
async def create_user(
    user_dto: UserRequestDTO = Body(...),
    create_user_service: CreateUserService = Depends(CreateUserService),
    db: AsyncSession = Depends(get_db)
):
    user_entity = user_dto.to_entity()
    return await create_user_service.create(user_entity, db)

@router.get("/users", status_code=status.HTTP_200_OK, response_model=Pageable[UserResponseDTO])
async def get_users(
    _offset: int = 0,
    _limit: int = 10,
    _sort: str = "+name",
    get_users_service: GetUsersService = Depends(GetUsersService),
    db: AsyncSession = Depends(get_db)
):
    return await get_users_service.get(_offset, _limit, _sort, db)
from uuid import UUID
from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.use_cases.create_user import CreateUser
from src.domain.use_cases.get_all_users import GetAllUsers
from src.domain.use_cases.get_user_by_id import GetUserById
from src.domain.use_cases.update_user import UpdateUser
from src.domain.use_cases.delete_user_by_id import DeleteUserById
from src.app.data_transfer_objects.user_request_dto import UserRequestDTO
from src.app.services.create_user_service import CreateUserService
from src.app.services.get_all_users_service import GetAllUsersService
from src.app.services.get_user_by_id_service import GetUserByIdService
from src.app.services.update_user_service import UpdateUserService
from src.app.services.delete_user_by_id_service import DeleteUserByIdService
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
async def get_all_users(
    offset: int = 0,
    limit: int = 10,
    sort: str = "+name",
    get_all_users_use_case: GetAllUsers = Depends(GetAllUsersService),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_users_use_case.get_all(offset, limit, sort, db)

@router.get("/users/{id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(
    id: UUID,
    get_user_by_id_use_case: GetUserById = Depends(GetUserByIdService),
    db: AsyncSession = Depends(get_db)
):
    return await get_user_by_id_use_case.get_by_id(id, db)

@router.put("/users/{id}", status_code=status.HTTP_200_OK)
async def update_user(
    id: UUID,
    user_dto: UserRequestDTO = Body(...),
    update_user_use_case: UpdateUser = Depends(UpdateUserService),
    db: AsyncSession = Depends(get_db)
):
    user_entity = user_dto.to_entity()
    user_entity.id = id
    return await update_user_use_case.update(user_entity, db)

@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    id: UUID,
    delete_user_by_id_use_case: DeleteUserById = Depends(DeleteUserByIdService),
    db: AsyncSession = Depends(get_db)
):
    return await delete_user_by_id_use_case.delete_by_id(id, db)

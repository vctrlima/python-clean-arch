from uuid import UUID
from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_transfer_objects.user_pageable_response_dto import UserPageableResponseDTO
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from domain.models.pageable_model import Pageable
from domain.use_cases.create_user import CreateUser
from domain.use_cases.get_all_users import GetAllUsers
from domain.use_cases.get_user_by_id import GetUserById
from domain.use_cases.update_user import UpdateUser
from domain.use_cases.delete_user_by_id import DeleteUserById
from app.data_transfer_objects.user_request_dto import UserRequestDTO
from app.services.create_user_service import CreateUserService
from app.services.get_all_users_service import GetAllUsersService
from app.services.get_user_by_id_service import GetUserByIdService
from app.services.update_user_service import UpdateUserService
from app.services.delete_user_by_id_service import DeleteUserByIdService
from infra.authorization.jwt_bearer import JWTBearer
from infra.persistence.adapters.db_connection import get_db

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseDTO,
)
async def create_user(
    user_dto: UserRequestDTO = Body(...),
    create_user_use_case: CreateUser = Depends(CreateUserService),
    db: AsyncSession = Depends(get_db),
):
    user_entity = user_dto.to_entity()
    return await create_user_use_case.create(user_entity, db)


@router.get(
    "/",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_200_OK,
    response_model=UserPageableResponseDTO,
)
async def get_all_users(
    offset: int = 0,
    limit: int = 10,
    sort: str = "+name",
    get_all_users_use_case: GetAllUsers = Depends(GetAllUsersService),
    db: AsyncSession = Depends(get_db),
):
    pageable = await get_all_users_use_case.get_all(offset, limit, sort, db)
    return UserPageableResponseDTO.create(pageable=pageable)


@router.get(
    "/{user_id}",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
)
async def get_user_by_id(
    user_id: UUID,
    get_user_by_id_use_case: GetUserById = Depends(GetUserByIdService),
    db: AsyncSession = Depends(get_db),
):
    return await get_user_by_id_use_case.get_by_id(user_id, db)


@router.put(
    "/{user_id}",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
)
async def update_user(
    user_id: UUID,
    user_dto: UserRequestDTO = Body(...),
    update_user_use_case: UpdateUser = Depends(UpdateUserService),
    db: AsyncSession = Depends(get_db),
):
    user_entity = user_dto.to_entity()
    user_entity.id = user_id
    return await update_user_use_case.update(user_entity, db)


@router.delete(
    "/{user_id}",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_id(
    user_id: UUID,
    delete_user_by_id_use_case: DeleteUserById = Depends(DeleteUserByIdService),
    db: AsyncSession = Depends(get_db),
):
    return await delete_user_by_id_use_case.delete_by_id(user_id, db)

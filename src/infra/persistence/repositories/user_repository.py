import logging
from typing import Callable
from uuid import UUID
from sqlalchemy import asc, desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.user import User
from domain.use_cases.create_user import CreateUser
from domain.use_cases.get_all_users import GetAllUsers
from domain.use_cases.get_user_by_id import GetUserById
from domain.models.pageable_model import Pageable
from infra.encryption.password_encryption import PasswordEncryption
from infra.persistence.models.user_model import UserModel

logging.basicConfig(level=logging.INFO)


class UserRepository(CreateUser, GetAllUsers, GetUserById):
    _logger = logging.getLogger(__name__)

    async def create(self, user: User, db: AsyncSession) -> User:
        try:
            new_user = UserModel(
                user, PasswordEncryption.encrypt(password=user.password)
            )
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return User(
                id=new_user.id, name=new_user.name, email=new_user.email, password=None
            )
        except Exception as e:
            self._logger.exception(e)
            return None

    async def get_all(
        self, offset: int, limit: int, _sort: str, db: AsyncSession
    ) -> Pageable[User]:
        _order_by_field = getattr(UserModel, _sort[1:])
        _order_by = (
            asc(_order_by_field) if _sort.startswith("+") else desc(_order_by_field)
        )
        query = select(UserModel).order_by(_order_by).limit(limit).offset(offset)
        routine = await db.execute(query)
        users = [
            User(id=user.id, name=user.name, email=user.email, password=None)
            for user in await routine.scalars().all()
        ]
        total_elements_query = await db.execute(
            select(func.count()).select_from(UserModel)
        )
        total_elements = await total_elements_query.scalar()
        return Pageable.create(
            content=users,
            limit=limit,
            offset=offset,
            total_elements=total_elements,
            current_page_elements=len(users),
        )

    async def get_by_id(self, id: UUID, db: AsyncSession) -> User:
        try:
            found_user = await db.get(UserModel, id)
            if not found_user:
                raise Exception("User with ID {id} not found!")
            return User(
                id=found_user.id,
                name=found_user.name,
                email=found_user.email,
                password=None,
            )
        except Exception as e:
            self._logger.exception(e)
            return None

    async def update(self, user: User, db: AsyncSession) -> User:
        try:
            updatable_user = await db.get(UserModel, user.id)
            if not updatable_user:
                raise Exception("User with ID {user.id} not found!")
            updatable_user.name = user.name
            updatable_user.email = user.email
            updatable_user.password = PasswordEncryption.encrypt(password=user.password)
            await db.commit()
            return user
        except Exception as e:
            self._logger.exception(e)
            return None

    async def delete_by_id(self, id: UUID, db: AsyncSession) -> None:
        try:
            found_user = await db.get(UserModel, id)
            if not found_user:
                raise Exception("User with ID {id} not found!")
            await db.delete(found_user)
            await db.commit()
        except Exception as e:
            self._logger.exception(e)

from uuid import UUID
from sqlalchemy import asc, desc, select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.user import User
from src.domain.use_cases.create_user import CreateUser
from src.domain.use_cases.get_all_users import GetAllUsers
from src.domain.use_cases.get_user_by_id import GetUserById
from src.domain.models.pageable_model import Pageable
from src.infra.encryption.password_encryption import PasswordEncryption
from src.infra.persistence.models.user_model import UserModel

class UserRepository(CreateUser, GetAllUsers, GetUserById):
    async def create(self, user: User, db: AsyncSession) -> User:
        new_user = UserModel(user, PasswordEncryption.encrypt(user.password))
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return User(id=new_user.id, name=new_user.name, email=new_user.email, password=None)

    async def get_all(self, offset: int, limit: int, _sort: str, db: AsyncSession) -> Pageable[User]:
        _order_by_field = getattr(UserModel, _sort[1:])
        _order_by = asc(_order_by_field) if _sort.startswith("+") else desc(_order_by_field)
        query = select(UserModel).order_by(_order_by).limit(limit).offset(offset)
        routine = await db.execute(query)
        users = [User(id=user.id, name=user.name, email=user.email, password=None) for user in routine.scalars().all()]
        total_elements_query = await db.execute(select(func.count()).select_from(UserModel))
        total_elements = total_elements_query.scalar()
        return Pageable.create(content=users, limit=limit, offset=offset, total_elements=total_elements, current_page_elements=len(users))

    async def get_by_id(self, id: UUID, db: AsyncSession) -> User:
        try:
            found_user = await db.get(UserModel, id)
            return User(id=found_user.id, name=found_user.name, email=found_user.email, password=None)
        except SQLAlchemyError as e:
            return None
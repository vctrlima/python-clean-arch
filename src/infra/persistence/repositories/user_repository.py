from typing import List
from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.use_cases.create_user import CreateUser
from src.domain.use_cases.get_users import GetUsers
from src.domain.entities.user import User
from src.infra.persistence.models.user_model import UserModel

class UserRepository(CreateUser, GetUsers):
    async def create(self, user: User, db: AsyncSession) -> User:
        new_user = UserModel(user=user)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def get(self, _offset: int, _limit: int, _sort: str, db: AsyncSession) -> List[UserModel]:
        _order_by_field = getattr(UserModel, _sort[1:])
        _order_by = asc(_order_by_field) if _sort.startswith("+") else desc(_order_by_field)
        query = select(UserModel).order_by(_order_by).limit(_limit).offset(_offset)
        routine = await db.execute(query)
        return routine.scalars().all()

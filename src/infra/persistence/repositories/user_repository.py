from sqlalchemy import asc, desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.user import User
from src.domain.use_cases.create_user import CreateUser
from src.domain.use_cases.get_users import GetUsers
from src.domain.models.pageable_model import Pageable
from src.infra.persistence.models.user_model import UserModel

class UserRepository(CreateUser, GetUsers):
    async def create(self, user: User, db: AsyncSession) -> User:
        new_user = UserModel(user=user)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return User(id=new_user.id, name=new_user.name, email=new_user.email, password=None)

    async def get(self, offset: int, limit: int, _sort: str, db: AsyncSession) -> Pageable[User]:
        _order_by_field = getattr(UserModel, _sort[1:])
        _order_by = asc(_order_by_field) if _sort.startswith("+") else desc(_order_by_field)
        query = select(UserModel).order_by(_order_by).limit(limit).offset(offset)
        routine = await db.execute(query)
        users = [User(id=user.id, name=user.name, email=user.email, password=None) for user in routine.scalars().all()]
        total_elements_query = await db.execute(select(func.count()).select_from(UserModel))
        total_elements = total_elements_query.scalar()
        return Pageable.create(content=users, limit=limit, offset=offset, total_elements=total_elements, current_page_elements=len(users))

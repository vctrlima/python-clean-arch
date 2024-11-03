from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.user import User
from src.domain.use_cases.create_user import CreateUser
from src.infra.persistence.adapters.db_connection import get_db
from src.infra.persistence.models.user_model import UserModel

class UserRepository(CreateUser):
    async def create(self, user: User, db: AsyncSession) -> User:
        new_user = UserModel(user=user)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

import logging
from datetime import datetime
from sqlalchemy import UUID, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from infra.persistence.models.refresh_token_model import RefreshTokenModel


class RefreshTokenRepository:
    _logger = logging.getLogger(__name__)

    async def save(self, refresh_token: RefreshTokenModel, db: AsyncSession):
        try:
            found_refresh_token = await self.get_by_user_id(
                user_id=refresh_token.user_id, db=db
            )
            if not found_refresh_token:
                db.add(refresh_token)
            else:
                updatable_refresh_token = await db.get(
                    RefreshTokenModel, found_refresh_token.id
                )
                updatable_refresh_token.hashed_token = refresh_token.hashed_token
                updatable_refresh_token.updated_at = datetime.now()
            await db.commit()
        except Exception as e:
            self._logger.exception(e)

    async def get_by_hashed_token(self, hashed_token: str, db: AsyncSession):
        try:
            statement = select(RefreshTokenModel).where(
                RefreshTokenModel.hashed_token == hashed_token
            )
            found_refresh_token = (await db.execute(statement)).scalar_one_or_none()
            if not found_refresh_token:
                raise Exception("RefreshToken with hash {hashed_token} not found!")
            return found_refresh_token
        except Exception as e:
            self._logger.exception(e)
            return None

    async def get_by_user_id(self, user_id: UUID, db: AsyncSession):
        try:
            statement = select(RefreshTokenModel).where(
                RefreshTokenModel.user_id == user_id
            )
            found_refresh_token = (await db.execute(statement)).scalar_one_or_none()
            if not found_refresh_token:
                raise Exception("RefreshToken with ID {id} not found!")
            return found_refresh_token
        except Exception as e:
            self._logger.exception(e)
            return None

    async def delete_by_user_id(self, user_id: UUID, db: AsyncSession):
        try:
            query = delete(RefreshTokenModel).where(
                RefreshTokenModel.user_id == user_id
            )
            await db.execute(query)
            await db.commit()
        except Exception as e:
            self._logger.exception(e)
            return None

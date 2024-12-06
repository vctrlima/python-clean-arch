import uuid
from sqlalchemy import Column, UUID, DateTime, ForeignKey, String, func
from sqlalchemy.ext.declarative import declarative_base
from infra.persistence.models.user_model import UserModel

Base = declarative_base()


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID, primary_key=True, index=True)
    hashed_token = Column(String, index=True)
    user_id = Column(UUID, ForeignKey(UserModel.id))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    __mapper_args__ = {"eager_defaults": True}

    def __init__(self, hashed_token: str, user_id: UUID):
        self.id = uuid.uuid4()
        self.hashed_token = hashed_token
        self.user_id = user_id

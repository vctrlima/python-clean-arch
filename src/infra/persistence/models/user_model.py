from sqlalchemy import Column, UUID, String
from sqlalchemy.ext.declarative import declarative_base
from src.domain.entities.user import User
import uuid

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String, index=True)

    def __init__(self, user: User):
        self.id = uuid.uuid4()
        self.name = user.name
        self.email = user.email
        self.password = user.password

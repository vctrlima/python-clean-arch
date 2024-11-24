from pydantic import BaseModel
from domain.entities.user import User
from domain.models.credentials_model import Credentials


class Authentication(BaseModel):
    user: User
    credentials: Credentials

    @classmethod
    def create(cls, user: User, credentials: Credentials):
        return cls(user=user, credentials=credentials)

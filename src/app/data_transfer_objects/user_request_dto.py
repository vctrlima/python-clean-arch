from typing import Optional
from pydantic import BaseModel
from domain.entities.user import User


class UserRequestDTO(BaseModel):
    id: Optional[str] = ""
    name: str = ""
    email: str = ""
    password: str = ""

    def to_entity(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            password=self.password,
        )

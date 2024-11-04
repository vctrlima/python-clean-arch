from pydantic import BaseModel
from src.domain.entities.user import User

class UserRequestDTO(BaseModel):
    name: str = ""
    email: str = ""
    password: str = ""
    
    def to_entity(self) -> User:
        return User(
            name=self.name,
            email=self.email,
            password=self.password,
        )
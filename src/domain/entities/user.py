from dataclasses import dataclass, field
from uuid import UUID

@dataclass
class User:
    id: UUID = field(default_factory=UUID)
    name: str = ""
    email: str = ""
    password: str = ""

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password

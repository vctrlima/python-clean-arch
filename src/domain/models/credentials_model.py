from datetime import datetime
from pydantic import BaseModel


class Credentials(BaseModel):
    token: str
    timestamp: datetime

    @classmethod
    def create(cls, token: str):
        return cls(token=token, timestamp=datetime.now())

from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class Pageable(BaseModel, Generic[T]):
    content: List[T]

    def __init__(self, content: List[T]):
        super().__init__(content=content)

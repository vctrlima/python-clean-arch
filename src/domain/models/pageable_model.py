from typing import Generic, TypeVar, List
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class Pageable(BaseModel, Generic[T]):
    content: List[T] = Field(..., alias="_content")
    limit: int = Field(..., alias="_limit")
    offset: int = Field(..., alias="_offset")
    page_number: int = Field(..., alias="_pageNumber")
    page_elements: int = Field(..., alias="_pageElements")
    total_pages: int = Field(..., alias="_totalPages")
    total_elements: int = Field(..., alias="_totalElements")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def create(
        cls,
        content: List[T],
        limit: int,
        offset: int,
        total_elements: int,
        current_page_elements: int,
    ):
        page_number = (offset // limit) + 1 if limit > 0 else 1
        total_pages = (total_elements + limit - 1) // limit if limit > 0 else 1
        return cls(
            _content=content,
            _limit=limit,
            _offset=offset,
            _pageNumber=page_number,
            _pageElements=current_page_elements,
            _totalPages=total_pages,
            _totalElements=total_elements,
        )

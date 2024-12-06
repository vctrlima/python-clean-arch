from typing import List
from pydantic import BaseModel, ConfigDict, Field
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from domain.models.pageable_model import Pageable


class UserPageableResponseDTO(BaseModel):
    content: List[UserResponseDTO] = Field(..., alias="_content")
    limit: int = Field(..., alias="_limit")
    offset: int = Field(..., alias="_offset")
    page_number: int = Field(..., alias="_pageNumber")
    page_elements: int = Field(..., alias="_pageElements")
    total_pages: int = Field(..., alias="_totalPages")
    total_elements: int = Field(..., alias="_totalElements")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def create(cls, pageable: Pageable[UserResponseDTO]):
        return cls(
            _content=pageable.content,
            _limit=pageable.limit,
            _offset=pageable.offset,
            _pageNumber=pageable.page_number,
            _pageElements=pageable.page_elements,
            _totalPages=pageable.total_pages,
            _totalElements=pageable.total_elements,
        )

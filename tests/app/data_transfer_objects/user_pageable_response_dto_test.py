import pytest
from uuid import uuid4
from app.data_transfer_objects.user_response_dto import UserResponseDTO
from domain.models.pageable_model import Pageable
from app.data_transfer_objects.user_pageable_response_dto import UserPageableResponseDTO


@pytest.fixture
def sample_user_dto():
    return UserResponseDTO(id=uuid4(), name="John Doe", email="john.doe@example.com")


@pytest.fixture
def sample_user_pageable(sample_user_dto):
    return Pageable.create(
        content=[sample_user_dto],
        limit=10,
        offset=0,
        total_elements=1,
        current_page_elements=1,
    )


def test_user_pageable_response_dto_create(sample_user_pageable):
    response_dto = UserPageableResponseDTO.create(sample_user_pageable)

    assert response_dto.limit == sample_user_pageable.limit
    assert response_dto.offset == sample_user_pageable.offset
    assert response_dto.page_number == sample_user_pageable.page_number
    assert response_dto.page_elements == sample_user_pageable.page_elements
    assert response_dto.total_pages == sample_user_pageable.total_pages
    assert response_dto.total_elements == sample_user_pageable.total_elements
    assert len(response_dto.content) == len(sample_user_pageable.content)
    assert response_dto.content[0].id == sample_user_pageable.content[0].id
    assert response_dto.content[0].name == sample_user_pageable.content[0].name
    assert response_dto.content[0].email == sample_user_pageable.content[0].email


def test_user_pageable_response_dto_aliases(sample_user_pageable):
    response_dto = UserPageableResponseDTO.create(sample_user_pageable)

    assert response_dto.dict(by_alias=True)["_limit"] == sample_user_pageable.limit
    assert response_dto.dict(by_alias=True)["_offset"] == sample_user_pageable.offset
    assert (
        response_dto.dict(by_alias=True)["_pageNumber"]
        == sample_user_pageable.page_number
    )
    assert (
        response_dto.dict(by_alias=True)["_pageElements"]
        == sample_user_pageable.page_elements
    )
    assert (
        response_dto.dict(by_alias=True)["_totalPages"]
        == sample_user_pageable.total_pages
    )
    assert (
        response_dto.dict(by_alias=True)["_totalElements"]
        == sample_user_pageable.total_elements
    )
    assert response_dto.dict(by_alias=True)["_content"] == [
        user.dict(by_alias=True) for user in sample_user_pageable.content
    ]

from http import HTTPStatus

import pytest

from main.api.data_generators.model_generator import RandomModelGenerator
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from sqlalchemy.orm import Session

from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse
from main.db.repositories.user_repository import UserRepository


@pytest.fixture
def create_user_request():
    return RandomModelGenerator.generate(CreateUserRequest)


@pytest.fixture
def user_repository(db_session: Session):
    return UserRepository(db_session)

@pytest.fixture
def created_user(create_user_request: CreateUserRequest, api_manager):
    response = api_manager.admin_steps.create_user(create_user_request)

    assert response.status_code == HTTPStatus.OK, (f'Полученный статус= {response.status_code}, '
                                                   f'отличается от 200 OK')

    user = CreateUserResponse.model_validate(response.json())
    return user

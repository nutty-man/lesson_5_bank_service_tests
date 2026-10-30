from collections.abc import Callable
from http import HTTPStatus

import pytest

from main.api.classes.api_manager import ApiManager
from main.api.data_generators.model_generator import RandomModelGenerator
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from sqlalchemy.orm import Session

from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse
from main.db.repositories.user_repository import UserRepository
from main.utils.enums.role import Role


@pytest.fixture
def create_user_request():
    return RandomModelGenerator.generate(CreateUserRequest)

@pytest.fixture
def user_repository(db_session: Session):
    return UserRepository(db_session)


@pytest.fixture
def user_factory(
    create_user_request: CreateUserRequest,
    api_manager: ApiManager,
) -> Callable[..., CreateUserResponse]:
    def create(
        role: Role | None = None,
        user_data: CreateUserRequest | None = None,
    ) -> CreateUserResponse:
        data = user_data if user_data is not None else create_user_request

        if role is not None:
            data = data.model_copy(update={"role": role})

        return api_manager.admin_steps.create_user_validated(data)

    return create

@pytest.fixture
def created_user(user_factory):
    return user_factory(None)

@pytest.fixture
def created_credit_user(user_factory):
    return user_factory(Role.CREDIT_SECRET)

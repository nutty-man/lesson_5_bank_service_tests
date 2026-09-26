import pytest

from main.api.data_generators.model_generator import RandomModelGenerator
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from sqlalchemy.orm import Session

from main.db.repositories.user_repository import UserRepository


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest, )
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def user_repository(db_session: Session):
    return UserRepository(db_session)

import pytest
from main.utils.calc_utils.utils import get_candidate_id
from collections.abc import Callable
from main.api.classes.api_manager import ApiManager
from main.api.config.api_config import ApiConfig
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from tests.fixtures.cleanup import clean_user


@pytest.fixture
def api_manager(
        config: ApiConfig,
        created_obj,
        admin_credentials: LoginUserRequest):
    manager = ApiManager(
        config=config,
        created_obj=created_obj,
    )

    manager.authenticate(admin_credentials)

    yield manager

    manager.authenticate(admin_credentials)
    clean_user(created_obj, manager)
    manager.close_session()


@pytest.fixture(scope="session")
def admin_credentials(config: ApiConfig) -> LoginUserRequest:
    return LoginUserRequest(
        username=config.username,
        password=config.password
    )

@pytest.fixture
def nonexistent_id():
    def generate(
        find_by_id: Callable[[int], object | None],
        min_id: int,
        max_id: int,
    ) -> int:
        return get_candidate_id(
            find_by_id=find_by_id,
            min_id=min_id,
            max_id=max_id,
        )

    return generate

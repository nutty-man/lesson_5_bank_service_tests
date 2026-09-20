from http import HTTPStatus

import pytest

from main.api.classes.api_manager import ApiManager
from main.api.config.api_config import ApiConfig
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from tests.fixtures.cleanup import clean_user


@pytest.fixture
def api_manager(config: ApiConfig,
        created_obj,
        admin_credentials: LoginUserRequest):

    manager = ApiManager(
        config=config,
        created_obj=created_obj,
    )
    manager.authenticate(
        admin_credentials,
        expected_status=HTTPStatus.OK,
    )

    yield manager

    manager.authenticate(
        admin_credentials,
        expected_status=HTTPStatus.OK,
    )
    clean_user(created_obj, manager)
    manager.close_session()

import pytest

from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse
from main.utils.enums.role import Role


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager, admin_credentials):
        response = api_manager.authenticate(admin_credentials)

        assert admin_credentials.username == response.user.username, (f'Имя пользователя отличается, '
                                                                      f'полученное имя= {response.username}')

        assert response.user.role == Role.ADMIN, (f'Роль отличается, '
                                                  f'полученная роль= {response.username}')

    def test_login_user(self, api_manager,
            create_user_request: CreateUserRequest,
            created_user: CreateUserResponse
    ):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, (f'Имя пользователя отличается '
                                                                        f'от ожидаемого {create_user_request.username}, '
                                                                        f'полученное имя= {response.username}')
        assert Role.USER == response.user.role, (f'Роль отличается от ожидаемой= {Role.USER}, '
                                                 f'полученная роль= {response.username}')

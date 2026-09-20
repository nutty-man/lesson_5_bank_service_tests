import pytest

from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.utils.enums.role import Role


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager):
        login_user_request = LoginUserRequest(username='admin', password='')
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.username, (f'Имя пользователя отличается, '
                                                                  f'полученное имя= {response.username}')
        assert response.user.role == Role.ADMIN, (f'Роль отличается, '
                                                                  f'полученная роль= {response.username}')

    def test_login_user(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, (f'Имя пользователя отличается, '
                                                                  f'полученное имя= {response.username}')
        assert response.user.role == Role.USER, (f'Роль отличается, '
                                                                  f'полученная роль= {response.username}')


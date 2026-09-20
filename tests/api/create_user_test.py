from http import HTTPStatus

import pytest

from main.api.classes.api_manager import ApiManager
from main.api.data_generators.model_generator import RandomModelGenerator
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.utils.enums.role import Role

from main.db.repositories.user_repository import UserRepository


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        'create_user_request',
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager: ApiManager,
                               create_user_request: CreateUserRequest, user_repository: UserRepository):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert response.status == HTTPStatus.OK, f'Полученный статус= {response.status}, отличается от 200 ОК'

        assert create_user_request.username == response.username, (f'Имя польз-ля невалидное, '
                                                                   f'полученное имя в ответе= {response.username}')
        assert create_user_request.role == response.role, (f'Роль польз-ля невалидна, '
                                                           f'полученная в ответе роль= {response.role}')

        user_from_db = user_repository.get_user_by_username(create_user_request.username)

        assert user_from_db.username == create_user_request.username, 'Созданного пользователя нет в БД'

    # @pytest.mark.parametrize(
    #     'username, password',
    #     [
    #         (),
    #         (),
    #         (),
    #         (),
    #         (),
    #         (),
    #         (),
    #         (),
    #         ()
    #     ]
    # )
    # def test_create_user_invalid(self, username: str, password: str, api_manager: ApiManager, user_repository: UserRepository):
    #     create_user_request = CreateUserRequest(username='tst', password='tst', role=Role.USER)
    #
    #     api_manager.admin_steps.create_invalid_user(create_user_request)
    #
    #     user_from_db = user_repository.get_user_by_username(create_user_request.username)
    #
    #     assert user_from_db is None, 'Пользователь создан, ошибка'

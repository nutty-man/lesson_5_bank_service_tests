from http import HTTPStatus

import allure
import pytest

from main.api.classes.api_manager import ApiManager
from main.api.data_generators.model_generator import RandomModelGenerator
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse

from main.db.repositories.user_repository import UserRepository
from main.utils.enums.role import Role


@pytest.mark.api
class TestCreateUser:

    @allure.story("Создание пользователя")
    @allure.title("Успешное создание пользователя")
    @pytest.mark.parametrize(
        'create_user_request',
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager: ApiManager,
                               create_user_request: CreateUserRequest, user_repository: UserRepository,
                               created_user):

        assert create_user_request.username == created_user.username, (
            f'Имя польз-ля невалидное, ожидалось= {create_user_request.username}'
            f'полученное имя в ответе= {created_user.username}')
        assert create_user_request.role == created_user.role, (f'Роль польз-ля невалидна, '
                                                       f'ожидалась {create_user_request.role}'
                                                       f'полученная в ответе роль= {created_user.role}')

        user_from_db = user_repository.get_user_by_username(create_user_request.username)

        assert user_from_db is not None, 'Созданный пользователь не найден в БД'

        assert user_from_db.username == create_user_request.username, (f'В БД ожидалось имя '
                                                                       f'{create_user_request.username}, '
                                                                       f'получено {user_from_db.username}')

    @allure.story("Создание пользователя")
    @allure.title("Некорректное создание пользователя")
    @pytest.mark.parametrize(
        'username, password',
        [
            ("ab", "ABCd12!$_!"),
            ("abcdefghijklmnop", "ABCd12!$_!"),
            ("user_name", "ABCd12!$_!"),
            ("юзер", "ABCd12!$_!"),
            ("user name", "ABCd12!$_!"),
            ("validUser2", "ABCD12!$_!")
        ]
    )
    def test_create_user_invalid(self,
                                 username: str, password: str,
                                 api_manager: ApiManager,
                                 user_repository: UserRepository):
        create_user_request = CreateUserRequest(username=username, password=password)

        response = api_manager.admin_steps.create_invalid_user(create_user_request)
        assert response.status_code == HTTPStatus.BAD_REQUEST, \
            (f'Полученный статус= {response.status_code},'
             f' ожидался {HTTPStatus.BAD_REQUEST}')

        user_from_db = user_repository.get_user_by_username(create_user_request.username)

        assert user_from_db is None, 'Пользователь создан, ошибка'

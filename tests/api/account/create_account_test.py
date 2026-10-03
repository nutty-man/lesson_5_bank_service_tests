from http import HTTPStatus

import pytest
import allure
from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.db.repositories.account_repository import AccountRepository


@pytest.mark.api
class TestCreateAccount:

    @allure.story("Создание счёта")
    @allure.title("Успешное создание банковского счёта пользователем")
    def test_create_account(self, api_manager: ApiManager, created_account,
                            account_repository: AccountRepository):
        assert created_account.balance == 0

        account_from_db = account_repository.get_account_by_id(created_account.id)

        assert account_from_db.id == created_account.id, (f'Аккаунт не создан, id аккаунта нет в DB,'
                                                          f'полученный id = {created_account.id}')
        assert account_from_db.balance is not None, (f'Поле баланса отсутствует в БД, '
                                                     f'баланс счёта= {account_from_db.balance}')

    @allure.story("Создание счёта")
    @allure.title("Запрет создания счёта пользователем с ролью ADMIN")
    def test_create_account_by_admin(self, api_manager: ApiManager):
        response = api_manager.user_steps.create_account()

        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'Ожидался статус {HTTPStatus.FORBIDDEN}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Создание счёта")
    @allure.title("Запрет создания более, чем двух счетов")
    def test_create_account_when_limit_reached(self, api_manager: ApiManager, created_user,
                                               create_user_request: CreateUserRequest,
                                               account_repository: AccountRepository):
        user_credentials = LoginUserRequest(
            username=create_user_request.username,
            password=create_user_request.password
        )

        api_manager.authenticate(user_credentials)

        first_response = api_manager.user_steps.create_account()

        assert first_response.status_code == HTTPStatus.CREATED, \
            (f'Полученный статус {first_response.status_code}'
             f'отличается от ожидаемого {HTTPStatus.CREATED}')

        first_account = CreateAccountResponse.model_validate(first_response.json())

        assert account_repository.get_account_by_id(first_account.id) is not None, \
            f'Ошибка создания аккаунта {first_account}'

        second_response = api_manager.user_steps.create_account()

        assert second_response.status_code == HTTPStatus.CREATED, \
            (f'Полученный статус {second_response.status_code}'
             f'отличается от ожидаемого {HTTPStatus.CREATED}')

        second_account = CreateAccountResponse.model_validate(second_response.json())

        assert account_repository.get_account_by_id(second_account.id) is not None, \
            f'Ошибка создания аккаунта {second_account}'

        response = api_manager.user_steps.create_account()

        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Полученный статус {response.status_code}'
             f'отличается от ожидаемого {HTTPStatus.CONFLICT}')

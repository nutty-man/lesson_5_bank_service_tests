from http import HTTPStatus

import pytest
import allure
from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.db.repositories.account_repository import AccountRepository


@pytest.mark.api
class TestCreateAccount:

    @allure.story("Создание счёта")
    @allure.title("Успешное создание банковского счёта пользователем")
    def test_create_account(self,
                            created_account: CreateAccountResponse,
                            account_repository: AccountRepository):
        assert created_account.balance == 0

        account_from_db = account_repository.get_account_by_id(created_account.id)

        assert account_from_db is not None, (
            f"Счёт {created_account.id} не найден в БД"
        )

        assert account_from_db.id == created_account.id, \
            (f'Аккаунт не создан, id аккаунта нет в DB,'
             f'полученный id = {created_account.id}')
        assert account_from_db.balance is not None, \
            (f'Поле баланса отсутствует в БД, '
             f'баланс счёта= {account_from_db.balance}')

    @allure.story("Создание счёта")
    @allure.title("Запрет создания счёта пользователем с ролью ADMIN")
    def test_create_account_by_admin(self, api_manager: ApiManager):
        response = api_manager.user_steps.create_account(HTTPStatus.FORBIDDEN)

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Создание счёта")
    @allure.title("Запрет создания более, чем двух счетов")
    def test_create_account_when_limit_reached(
            self,
            api_manager: ApiManager,
            user_with_two_accounts,
    ):
        response = api_manager.user_steps.create_account(HTTPStatus.CONFLICT)

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

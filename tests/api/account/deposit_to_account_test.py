from collections.abc import Callable
from http import HTTPStatus
import random

import pytest
import allure

from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.api.specs.request_specs import RequestSpecs
from main.db.repositories.account_repository import AccountRepository


@pytest.mark.api
class TestDepositToAccount:

    @allure.story("Пополнение счёта")
    @allure.title("Успешное пополнение счёта")
    def test_deposit_to_account_valid(
            self,
            api_manager: ApiManager,
            created_account: CreateAccountResponse,
            deposit_data_factory: Callable[[int | str], AccountDepositRequest],
            account_repository: AccountRepository,
    ):
        data = deposit_data_factory(created_account.id)

        api_manager.user_steps.deposit_to_account_validated(data)

        account_from_db = account_repository.get_account_by_id(created_account.id)

        assert account_from_db is not None
        assert account_from_db.balance == data.amount, \
            (f'Полученный баланс некорректен, ожидался = {data.amount}'
             f' баланс счёта= {account_from_db.balance}')

    @allure.story("Пополнение счёта")
    @allure.title("Пополнение счёта при несуществующем accountId")
    def test_no_account_id(
            self,
            api_manager: ApiManager,
            created_account: CreateAccountResponse,
            nonexistent_account_id: Callable[[int, int], int],
            deposit_data_factory: Callable[[int | str], AccountDepositRequest],
    ):
        data = deposit_data_factory(nonexistent_account_id(1, 9999))

        response = api_manager.user_steps.deposit_to_account(
            data,
            HTTPStatus.NOT_FOUND,
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Пополнение счёта")
    @allure.title("Передача некорректного тела запроса")
    def test_deposit_invalid_body(
            self,
            api_manager: ApiManager,
            deposit_data_factory: Callable[[int | str], AccountDepositRequest],
    ):
        response = api_manager.user_steps.deposit_to_account(
            deposit_data_factory("invalid_id"),
            HTTPStatus.BAD_REQUEST,
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Пополнение счёта")
    @allure.title("Запрет на пополнение счёта без прав на операцию")
    def test_deposit_to_account_forbidden(self, api_manager: ApiManager,
                                          create_deposit_data: AccountDepositRequest):
        response = api_manager.user_steps.deposit_to_account(
            create_deposit_data,
            HTTPStatus.FORBIDDEN,
        )

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Пополнение счёта")
    @allure.title("Запрет на пополнение счёта не авторизованным пользователем")
    def test_deposit_to_account_unauth(self, api_manager: ApiManager,
                                       create_deposit_data: AccountDepositRequest):
        response = api_manager.user_steps.deposit_to_account(
            create_deposit_data,
            HTTPStatus.UNAUTHORIZED,
            headers=RequestSpecs.unauth_headers(),
        )

        response_body = response.json()

        assert "code" in response_body
        assert response_body["code"] == HTTPStatus.UNAUTHORIZED

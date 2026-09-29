from http import HTTPStatus
import random

import pytest
import allure

from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.specs.request_specs import RequestSpecs
from main.db.repositories.account_repository import AccountRepository


@pytest.mark.api
class TestDepositToAccount:

    @allure.story("Пополнение счёта")
    @allure.title("Успешное пополнение счёта")
    def test_deposit_to_account_valid(self, api_manager: ApiManager, created_account,
                                      create_deposit_data: AccountDepositRequest,
                                      account_repository: AccountRepository):
        data = create_deposit_data.model_copy(
            update={"accountId": created_account.id}
        )

        response = api_manager.user_steps.deposit_to_account(data)

        assert response.status_code == HTTPStatus.OK, (
            f'Ожидался статус {HTTPStatus.OK}, '
            f'получен {response.status_code}')

        account_from_db = account_repository.get_account_by_id(created_account.id)

        assert account_from_db.balance == data.amount, (f'Полученный баланс некорректен, ожидался = {data.amount}'
                                                        f'баланс счёта= {account_from_db.balance}')

    @allure.story("Пополнение счёта")
    @allure.title("Пополнение счёта при несуществующем accountId")
    def test_no_account_id(self, api_manager: ApiManager, created_account,
                           create_deposit_data: AccountDepositRequest,
                           account_repository: AccountRepository):

        while True:
            candidate_id = random.randint(1, 9999)
            account_from_db = account_repository.get_account_by_id(candidate_id)

            if account_from_db is None:
                break

        data = create_deposit_data.model_copy(
            update={"accountId": candidate_id}
        )

        response = api_manager.user_steps.deposit_to_account(data)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'Ожидался статус {HTTPStatus.NOT_FOUND}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Пополнение счёта")
    @allure.title("Передача некорректного тела запроса")
    def test_deposit_invalid_body(self, api_manager: ApiManager,
                                  create_deposit_data: AccountDepositRequest):
        data = create_deposit_data.model_copy(
            update={"accountId": "invalid_id"}
        )

        response = api_manager.user_steps.deposit_to_account(data)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Ожидался статус {HTTPStatus.BAD_REQUEST}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Пополнение счёта")
    @allure.title("Запрет на пополнение счёта без прав на операцию")
    def test_deposit_to_account_forbidden(self, api_manager: ApiManager,
                                          create_deposit_data: AccountDepositRequest):
        response = api_manager.user_steps.deposit_to_account(create_deposit_data)

        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'Ожидался статус {HTTPStatus.FORBIDDEN}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Пополнение счёта")
    @allure.title("Запрет на пополнение счёта не авторизованным пользователем")
    def test_deposit_to_account_unauth(self, api_manager: ApiManager,
                                          create_deposit_data: AccountDepositRequest):

        response = api_manager.user_steps.deposit_to_account(create_deposit_data,
                                                             headers=RequestSpecs.unauth_headers())

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'Ожидался статус {HTTPStatus.UNAUTHORIZED}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "code" in response_body
        assert response_body["code"] == HTTPStatus.UNAUTHORIZED

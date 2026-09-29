from http import HTTPStatus
import random

import pytest
import allure

from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.account.account_transfer_request import AccountTransferRequest
from main.api.schemas.dto.response.account.account_transfer_response import AccountTransferResponse
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.api.specs.request_specs import RequestSpecs
from main.db.repositories.account_repository import AccountRepository


@pytest.mark.api
class TestTransferToAccount:

    @allure.story("Перевод денег со счёта")
    @allure.title("Успешный перевод денег со счёта")
    def test_transfer_to_account_valid(self, api_manager: ApiManager, created_account,
                                       account_transfer_data: AccountTransferRequest,
                                       create_deposit_data: AccountDepositRequest,
                                       account_repository: AccountRepository):

        deposit_data = create_deposit_data.model_copy(
            update={"accountId": created_account.id}
        )

        deposited_account = api_manager.user_steps.deposit_to_account(deposit_data)

        assert deposited_account.status_code == HTTPStatus.OK, (
            f'Ожидался статус {HTTPStatus.OK}, '
            f'получен {deposited_account.status_code}')

        second_account = api_manager.user_steps.create_account()

        assert second_account.status_code == HTTPStatus.CREATED, \
            (f'Полученный статус {second_account.status_code}'
             f'отличается от ожидаемого {HTTPStatus.CREATED}')

        second_account = CreateAccountResponse.model_validate(second_account.json())

        data = account_transfer_data.model_copy(
            update={"fromAccountId": created_account.id,
                    "toAccountId": second_account.id,
                    "amount": deposit_data.amount}
        )

        response = api_manager.user_steps.transfer_to_account(data)

        assert response.status_code == HTTPStatus.OK, (
            f'Ожидался статус {HTTPStatus.OK}, '
            f'получен {response.status_code}')

        AccountTransferResponse.model_validate(response.json())

        account_from_db = account_repository.get_account_by_id(second_account.id)

        assert account_from_db.balance == data.amount, (f'Полученный баланс некорректен, '
                                                            f'ожидался = {data.amount}'
                                                            f'баланс счёта= {account_from_db.balance}')

    @allure.story("Перевод денег со счёта")
    @allure.title("Один из счетов не существует")
    def test_transfer_to_invalid_account(self, api_manager: ApiManager, created_account,
                                          account_transfer_data: AccountTransferRequest,
                                          account_repository: AccountRepository):
        while True:
            candidate_id = random.randint(1, 9999)
            account_from_db = account_repository.get_account_by_id(candidate_id)

            if account_from_db is None:
                break

        data = account_transfer_data.model_copy(
            update={"fromAccountId": candidate_id,
                    "toAccountId": created_account.id}
        )

        response = api_manager.user_steps.transfer_to_account(data)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'Ожидался статус {HTTPStatus.NOT_FOUND}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Перевод денег со счёта")
    @allure.title("Недостаточно средств или сумма перевода превышена")
    def test_transfer_to_account_insufficient_amount(self, api_manager: ApiManager, created_account,
                                                     account_transfer_data: AccountTransferRequest,
                                                     account_repository: AccountRepository):

        second_account = api_manager.user_steps.create_account()
        assert second_account.status_code == HTTPStatus.CREATED, \
            (f'Полученный статус {second_account.status_code}'
             f'отличается от ожидаемого {HTTPStatus.CREATED}')

        second_account = CreateAccountResponse.model_validate(second_account.json())

        data = account_transfer_data.model_copy(
            update={"fromAccountId": second_account.id,
                    "toAccountId": created_account.id}
        )

        response = api_manager.user_steps.transfer_to_account(data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
            f'Ожидался статус {HTTPStatus.UNPROCESSABLE_ENTITY}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Перевод денег со счёта")
    @allure.title("Запрет на перевод со счёта не авторизованным пользователем")
    def test_transfer_to_account_unauth(self, api_manager: ApiManager,
                                        account_transfer_data: AccountTransferRequest, ):

        response = api_manager.user_steps.transfer_to_account(account_transfer_data,
                                                              headers=RequestSpecs.unauth_headers())

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'Ожидался статус {HTTPStatus.UNAUTHORIZED}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "code" in response_body
        assert response_body["code"] == HTTPStatus.UNAUTHORIZED

    @allure.story("Перевод денег со счёта")
    @allure.title("Некорректное тело запроса")
    def test_transfer_to_account_invalid_body(self, api_manager: ApiManager,
                                  account_transfer_data: AccountTransferRequest):
        data = account_transfer_data.model_copy(
            update={"fromAccountId": "invalid_id"}
        )

        response = api_manager.user_steps.transfer_to_account(data)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Ожидался статус {HTTPStatus.BAD_REQUEST}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Перевод денег со счёта")
    @allure.title("У пользователя нет прав для осуществления операции")
    def test_transfer_to_account_forbidden(self, api_manager: ApiManager,
                                          account_transfer_data: AccountTransferRequest):
        response = api_manager.user_steps.transfer_to_account(account_transfer_data)

        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'Ожидался статус {HTTPStatus.FORBIDDEN}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

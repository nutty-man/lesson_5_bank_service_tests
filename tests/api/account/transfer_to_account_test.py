from collections.abc import Callable
from http import HTTPStatus

import pytest
import allure

from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.request.account.account_transfer_request import AccountTransferRequest
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.api.specs.request_specs import RequestSpecs
from main.db.repositories.account_repository import AccountRepository


@pytest.mark.api
class TestTransferToAccount:

    @allure.story("Перевод денег со счёта")
    @allure.title("Успешный перевод денег со счёта")
    def test_transfer_to_account_valid(
            self,
            api_manager: ApiManager,
            funded_accounts: tuple[CreateAccountResponse, CreateAccountResponse, float],
            transfer_data_factory: Callable[..., AccountTransferRequest],
            account_repository: AccountRepository,
    ):
        first_account, second_account, amount = funded_accounts

        data = transfer_data_factory(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=amount,
        )

        api_manager.user_steps.transfer_to_account_validated(data)

        account_from_db = account_repository.get_account_by_id(second_account.id)

        assert account_from_db is not None
        assert account_from_db.balance == data.amount

    @allure.story("Перевод денег со счёта")
    @allure.title("Один из счетов не существует")
    def test_transfer_to_invalid_account(
            self,
            api_manager: ApiManager,
            created_account: CreateAccountResponse,
            nonexistent_account_id: Callable[[int, int], int],
            transfer_data_factory: Callable[..., AccountTransferRequest],
    ):
        data = transfer_data_factory(
            fromAccountId=nonexistent_account_id(1, 9999),
            toAccountId=created_account.id,
        )

        response = api_manager.user_steps.transfer_to_account(
            data, HTTPStatus.NOT_FOUND
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Перевод денег со счёта")
    @allure.title("Недостаточно средств или сумма перевода превышена")
    def test_transfer_to_account_insufficient_amount(
            self,
            api_manager: ApiManager,
            user_with_two_accounts: tuple[
                CreateAccountResponse, CreateAccountResponse
            ],
            transfer_data_factory: Callable[..., AccountTransferRequest],
    ):
        first_account, second_account = user_with_two_accounts

        data = transfer_data_factory(
            fromAccountId=second_account.id,
            toAccountId=first_account.id,
        )

        response = api_manager.user_steps.transfer_to_account(
            data, HTTPStatus.UNPROCESSABLE_ENTITY
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Перевод денег со счёта")
    @allure.title("Запрет на перевод со счёта не авторизованным пользователем")
    def test_transfer_to_account_unauth(
            self,
            api_manager: ApiManager,
            account_transfer_data: AccountTransferRequest,
    ):
        response = api_manager.user_steps.transfer_to_account(
            account_transfer_data,
            HTTPStatus.UNAUTHORIZED,
            headers=RequestSpecs.unauth_headers(),
        )

        response_body = response.json()
        assert "code" in response_body
        assert response_body["code"] == HTTPStatus.UNAUTHORIZED

    @allure.story("Перевод денег со счёта")
    @allure.title("Некорректное тело запроса")
    def test_transfer_to_account_invalid_body(
            self,
            api_manager: ApiManager,
            transfer_data_factory: Callable[..., AccountTransferRequest],
    ):
        response = api_manager.user_steps.transfer_to_account(
            transfer_data_factory(fromAccountId="invalid_id"),
            HTTPStatus.BAD_REQUEST,
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Перевод денег со счёта")
    @allure.title("У пользователя нет прав для осуществления операции")
    def test_transfer_to_account_forbidden(
            self,
            api_manager: ApiManager,
            account_transfer_data: AccountTransferRequest,
    ):
        response = api_manager.user_steps.transfer_to_account(
            account_transfer_data,
            HTTPStatus.FORBIDDEN,
        )

        response_body = response.json()
        assert "error" in response_body
        assert response_body["error"]

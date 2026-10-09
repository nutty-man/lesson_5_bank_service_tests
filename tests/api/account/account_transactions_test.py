from http import HTTPStatus

import pytest
import allure
import random

from main.api.classes.api_manager import ApiManager
from main.api.schemas.context.transaction_history_context import TransactionHistoryContext
from main.api.specs.request_specs import RequestSpecs
from main.db.repositories.account_repository import AccountRepository
from main.utils.calc_utils.utils import get_transaction_types, round_balance


@pytest.mark.api
class TestAccountTransactions:

    @allure.story("Получение истории транзакций для указанного счета")
    @allure.title("Успешное получение истории транзакций для указанного счета")
    def test_account_transactions(
            self,
            api_manager: ApiManager,
            prepared_transaction_history: TransactionHistoryContext,
    ):

        response = api_manager.user_steps.get_transactions_history_validated(
            prepared_transaction_history.account.id
        )

        expected_balance = prepared_transaction_history.expected_balance

        account = prepared_transaction_history.account

        assert response.id == account.id, \
            (f'Полученный id= {response.id} '
             f'не соответствует ожидаемому= {account.id}')
        assert response.number == account.number, \
            (f'Полученный номер счёта= {response.number} '
             f'не соответствует ожидаемому= {account.number}')
        assert round_balance(response.balance) == round_balance(expected_balance), (
            f"Полученный баланс={response.balance} "
            f"не соответствует ожидаемому={expected_balance}"
        )

        types = get_transaction_types(response.transactions)

        assert "transfer_out" in types
        assert "deposit" in types

    @pytest.mark.xfail(
        reason="BUG: для невалидного account ID API возвращает 500 вместо 400",
        strict=True
    )
    @allure.story("Получение истории транзакций для указанного счета")
    @allure.title("Неверный формат ID")
    def test_account_transactions_with_invalid_id(self, api_manager: ApiManager):
        response = api_manager.user_steps.get_transactions_history('12abc')

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Ожидался статус {HTTPStatus.BAD_REQUEST}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

    @allure.story("Получение истории транзакций для указанного счета")
    @allure.title("Пользователь не авторизован")
    def test_account_transactions_unauth(self, api_manager, created_account):
        response = api_manager.user_steps.get_transactions_history(
            created_account.id,
            headers=RequestSpecs.unauth_headers())

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'Ожидался статус {HTTPStatus.UNAUTHORIZED}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "code" in response_body
        assert response_body["code"] == HTTPStatus.UNAUTHORIZED

    @allure.story("Получение истории транзакций для указанного счета")
    @allure.title("Аккаунт с указанным id не найден или не принадлежит пользователю")
    def test_account_transactions_account_not_found(self, api_manager: ApiManager, created_account,
                                                    account_repository: AccountRepository,
                                                    nonexistent_account_id):

        candidate_id = nonexistent_account_id(1, 9999)

        response = api_manager.user_steps.get_transactions_history(candidate_id)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'Ожидался статус {HTTPStatus.NOT_FOUND}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

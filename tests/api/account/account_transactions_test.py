from http import HTTPStatus

import pytest
import allure
import random

from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.account.account_transfer_request import AccountTransferRequest
from main.api.schemas.dto.response.account.account_transactions_response import AccountTransactionsResponse
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.api.specs.request_specs import RequestSpecs
from main.db.repositories.account_repository import AccountRepository


@pytest.mark.api
class TestAccountTransactions:

    @allure.story("Получение истории транзакций для указанного счета")
    @allure.title("Успешное получение истории транзакций для указанного счета")
    def test_account_transactions(self, api_manager: ApiManager, created_account,
                                  account_repository: AccountRepository,
                                  create_deposit_data: AccountDepositRequest,
                                  account_transfer_data: AccountTransferRequest,):
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
                    "amount": random.uniform(500, deposit_data.amount - 1)}
        )

        api_manager.user_steps.transfer_to_account(data)

        response = api_manager.user_steps.get_transactions_history(created_account.id)

        response = AccountTransactionsResponse.model_validate(response.json())

        expected_balance = deposit_data.amount - data.amount

        assert response.id == created_account.id, \
            (f'Полученный id= {response.id} '
             f'не соответствует ожидаемому= {created_account.id}')
        assert response.number == created_account.number, \
            (f'Полученный номер счёта= {response.number} '
             f'не соответствует ожидаемому= {created_account.number}')
        assert round(response.balance) == round(expected_balance), \
            (f'Полученный баланс= {round(response.balance)} '
             f'не соответствует ожидаемому= {round(expected_balance)}')

        transactions = response.transactions
        types = []
        for t in transactions:
            types.append(t.type)
        assert 'transfer_out' in set(types), (f'Транзакция с типом transfer_out не найдена, '
                                              f'получено: {types}')
        assert 'deposit' in set(types), (f'Транзакция с типом deposit не найдена, '
                                              f'получено: {types}')

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
                                          account_repository: AccountRepository):
        while True:
            candidate_id = random.randint(1, 9999)
            account_from_db = account_repository.get_account_by_id(candidate_id)

            if account_from_db is None:
                break

        response = api_manager.user_steps.get_transactions_history(candidate_id)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'Ожидался статус {HTTPStatus.NOT_FOUND}, '
            f'получен {response.status_code}')

        response_body = response.json()

        assert "error" in response_body
        assert response_body["error"]

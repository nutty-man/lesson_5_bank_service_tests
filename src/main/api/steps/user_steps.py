from http import HTTPStatus
from typing import Optional
from collections.abc import Callable
from requests import Response

import allure

from main.api.clients.account_api import AccountApi
from main.api.clients.credit_api import CreditApi
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.account.account_transfer_request import AccountTransferRequest
from main.api.schemas.dto.request.credit.create_credit_repay_request import CreateCreditRepayRequest
from main.api.schemas.dto.request.credit.create_credit_request import CreateCreditRequest
from main.api.schemas.dto.response.account.account_transactions_response import AccountTransactionsResponse
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse
from main.api.specs.response_specs import ResponseSpecs


class UserSteps:
    def __init__(self, account_api: AccountApi, credit_api: CreditApi):
        self.account_api = account_api
        self.credit_api = credit_api

    def create_account(self, expected_status: HTTPStatus) -> Response:
        return self.account_api.create_account(
            response_spec=ResponseSpecs.check_status(expected_status),
        )

    @allure.step("Создать счёт пользователя с проверкой ответа")
    def create_account_validated(self) -> CreateAccountResponse:
        return self.account_api.create_account(
            response_spec=ResponseSpecs.check_status(HTTPStatus.CREATED),
            response_model=CreateAccountResponse,
        )

    def deposit_to_account(
            self,
            data: AccountDepositRequest,
            expected_status: HTTPStatus,
            headers: dict | None = None,
    ) -> Response:
        return self.account_api.deposit_to_account(
            data,
            headers=headers,
            response_spec=ResponseSpecs.check_status(expected_status),
        )

    @allure.step("Пополнить счёт пользователя с проверкой ответа")
    def deposit_to_account_validated(
            self,
            deposit_data: AccountDepositRequest,
    ):
        return self.account_api.deposit_to_account(
            deposit_data,
            response_spec=ResponseSpecs.check_status(HTTPStatus.OK),
        )

    @allure.step("Перевести деньги с одного счёта на другой")
    def transfer_to_account(self,
                            transfer_data: AccountTransferRequest,
                            expected_status: HTTPStatus,
                            headers: Optional[dict] = None):
        return self.account_api.transfer_to_account(transfer_data,
            headers=headers,
            response_spec=ResponseSpecs.check_status(expected_status),
        )

    @allure.step("Перевести деньги с одного счёта на другой с проверкой ответа")
    def transfer_to_account_validated(
            self,
            transfer_data: AccountTransferRequest,
    ):
        return self.account_api.transfer_to_account(
            transfer_data,
            response_spec=ResponseSpecs.check_status(HTTPStatus.OK),
        )

    @allure.step("Получить историю транзакций счёта")
    def get_transactions_history(self, account_id, headers: Optional[dict] = None):
        return self.account_api.get_transactions_history(account_id, headers)

    @allure.step("Получить историю транзакций счёта с проверкой ответа")
    def get_transactions_history_validated(
            self,
            account_id: int,
    ) -> AccountTransactionsResponse:
        return self.account_api.get_transactions_history(
            account_id,
            response_spec=ResponseSpecs.check_status(HTTPStatus.OK),
            response_model=AccountTransactionsResponse,
        )

    @allure.step("Запросить кредит")
    def create_credit(self, credit_data: CreateCreditRequest,
                               headers: Optional[dict] = None):
        return self.credit_api.create_credit(credit_data, headers)

    @allure.step("Погасить кредит")
    def create_credit_repay(self, credit_data: CreateCreditRepayRequest,
                                     headers: Optional[dict] = None):
        return self.credit_api.create_credit_repay(credit_data, headers)

    @allure.step("Получить историю кредитов")
    def get_credit_history(self,
                           headers: Optional[dict] = None,
                           ):
        return self.credit_api.get_credit_history(headers)

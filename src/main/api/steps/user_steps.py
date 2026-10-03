from typing import Optional

import allure

from main.api.clients.account_api import AccountApi
from main.api.clients.credit_api import CreditApi
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.account.account_transfer_request import AccountTransferRequest
from main.api.schemas.dto.request.credit.create_credit_repay_request import CreateCreditRepayRequest
from main.api.schemas.dto.request.credit.create_credit_request import CreateCreditRequest


class UserSteps:
    def __init__(self, account_api: AccountApi, credit_api: CreditApi):
        self.account_api = account_api
        self.credit_api = credit_api

    @allure.step("Создать счёт пользователя")
    def create_account(self):
        return self.account_api.create_account()

    @allure.step("Пополнить счёт пользователя")
    def deposit_to_account(self,
                           deposit_data: AccountDepositRequest,
                           headers: Optional[dict] = None):
        return self.account_api.deposit_to_account(deposit_data, headers)

    @allure.step("Перевести деньги с одного счёта на другой")
    def transfer_to_account(self,
                            transfer_data: AccountTransferRequest,
                            headers: Optional[dict] = None):
        return self.account_api.transfer_to_account(transfer_data, headers)

    @allure.step("Получить историю транзакций счёта")
    def get_transactions_history(self, account_id, headers: Optional[dict] = None):
        return self.account_api.get_transactions_history(account_id, headers)

    @allure.step("Запросить кредит")
    def create_credit(self, credit_data: CreateCreditRequest,
                               headers: Optional[dict] = None):
        return self.credit_api.create_credit(credit_data, headers)

    @allure.step("Погасить кредит")
    def create_credit_repay(self, credit_data: CreateCreditRepayRequest,
                                     headers: Optional[dict] = None):
        return self.credit_api.create_credit_repay(credit_data, headers)

    @allure.step("Получить историю кредитов")
    def get_credit_history(self, headers: Optional[dict] = None):
        return self.credit_api.get_credit_history(headers)

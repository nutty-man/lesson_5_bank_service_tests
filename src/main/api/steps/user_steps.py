from http import HTTPStatus

import allure

from main.api.clients.account_api import AccountApi
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse


class UserSteps:
    def __init__(self, account_api: AccountApi):
        self.account_api = account_api

    @allure.step("Создать счёт пользователя")
    def create_account(self, expected_status: int | HTTPStatus) -> CreateAccountResponse:
        return self.account_api.create_account(expected_status=expected_status)

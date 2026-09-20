from http import HTTPStatus
from main.api.foundation.requester import Requester
from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse


class AccountApi:
    CREATE_ACCOUNT_ENDPOINT = "/account/create"

    def __init__(self, requester: Requester):
        self.requester = requester

    def create_account(self, expected_status: int | HTTPStatus) -> CreateAccountResponse:
        response = self.requester.send_request(
            method="POST",
            endpoint=self.CREATE_ACCOUNT_ENDPOINT,
            expected_status=expected_status,
        )
        return CreateAccountResponse.model_validate(response.json())

from http import HTTPStatus
from typing import Any

import requests

from main.api.clients.account_api import AccountApi
from main.api.clients.auth_api import AuthApi
from main.api.clients.transaction_api import TransactionApi
from main.api.clients.user_api import UserApi
from main.api.config.api_config import ApiConfig
from main.api.foundation.requester import Requester
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.api.schemas.dto.response.user.login_user_response import LoginUserResponse
from main.api.specs.request_specs import RequestSpecs
from main.api.steps.admin_steps import AdminSteps
from main.api.steps.user_steps import UserSteps


class ApiManager:
    def __init__(
        self,
        config: ApiConfig,
        created_obj: list[Any] | None = None,
    ):
        self.created_obj = created_obj if created_obj is not None else []
        self.session = requests.Session()
        self.requester = Requester(self.session, config)

        self.auth_api = AuthApi(self.requester)
        self.account_api = AccountApi(self.requester)
        self.user_api = UserApi(self.requester)
        self.transaction_api = TransactionApi(self.requester)

        self.admin_steps = AdminSteps(
            user_api=self.user_api,
            auth_api=self.auth_api,
            set_auth_token=self.set_auth_token,
            created_obj=self.created_obj,
        )

        self.user_steps = UserSteps(account_api=self.account_api)

    def set_auth_token(self, token: str) -> None:
        self.session.headers.update(RequestSpecs.auth_headers(token))

    def authenticate(self,
        credentials: LoginUserRequest,
        expected_status: int | HTTPStatus) -> LoginUserResponse:
        return self.admin_steps.login_user(credentials, expected_status)

    def clear_auth(self) -> None:
        self.session.headers.pop("Authorization", None)

    def close_session(self) -> None:
        self.session.close()

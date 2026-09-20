from http import HTTPStatus

from main.api.clients.base_api import BaseApi
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.api.schemas.dto.response.user.login_user_response import LoginUserResponse
from main.api.specs.request_specs import RequestSpecs


class AuthApi(BaseApi):
    LOGIN_ENDPOINT = "/auth/token/login"

    def login(
        self, credentials: LoginUserRequest,
        expected_status: int | HTTPStatus = HTTPStatus.OK) -> LoginUserResponse:
        response = self.requester.send_request(
            method="POST",
            endpoint=self.LOGIN_ENDPOINT,
            json_data=credentials.model_dump(mode="json"),
            headers=RequestSpecs.unauth_headers(),
            expected_status=expected_status,
        )

        return LoginUserResponse.model_validate(response.json())

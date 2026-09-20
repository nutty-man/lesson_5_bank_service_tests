from http import HTTPStatus

import requests

from main.api.clients.base_api import BaseApi
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse


class UserApi(BaseApi):
    CREATE_USER_ENDPOINT = "/admin/create"
    DELETE_USER_ENDPOINT = "/admin/users/{user_id}"

    def create_user(self, user_data: CreateUserRequest,
        expected_status: HTTPStatus) -> CreateUserResponse:
        response = self.requester.send_request(
            method="POST",
            endpoint=self.CREATE_USER_ENDPOINT,
            json_data=user_data.model_dump(mode="json"),
            expected_status=expected_status,
        )
        return CreateUserResponse.model_validate(response.json())

    def create_user_raw(
        self,
        user_data: CreateUserRequest,
        expected_status: int | HTTPStatus,
    ) -> requests.Response:
        return self.requester.send_request(
            method="POST",
            endpoint=self.CREATE_USER_ENDPOINT,
            json_data=user_data.model_dump(mode="json"),
            expected_status=expected_status,
        )

    def delete_user(self, user_id: int,
                    expected_status: int | HTTPStatus) -> requests.Response:
        endpoint = self.DELETE_USER_ENDPOINT.format(user_id=user_id)
        return self.requester.send_request(
            method="DELETE",
            endpoint=endpoint,
            expected_status=expected_status,
        )

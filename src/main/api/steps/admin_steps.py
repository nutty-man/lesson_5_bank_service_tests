from http import HTTPStatus
from typing import Callable

import requests

from main.api.clients.auth_api import AuthApi
from main.api.clients.user_api import UserApi
from main.api.schemas.dto.request.user.login_user_request import LoginUserRequest
from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse
from main.api.schemas.dto.response.user.login_user_response import LoginUserResponse
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.api.steps.base_steps import BaseSteps

import allure


class AdminSteps(BaseSteps):
    def __init__(self,
            user_api: UserApi,
            auth_api: AuthApi,
            set_auth_token: Callable[[str], None],
            created_obj: list):
        super().__init__(created_obj)
        self.user_api = user_api
        self.auth_api = auth_api
        self.set_auth_token = set_auth_token

    @allure.step("Авторизация пользователя")
    def login_user(
            self,
            login_user_request: LoginUserRequest,
            expected_status: int | HTTPStatus,
    ) -> LoginUserResponse:
        response = self.auth_api.login(
            credentials=login_user_request,
            expected_status=expected_status,
        )
        self.set_auth_token(response.token)
        return response

    @allure.step("Создание пользователя")
    def create_user(
            self,
            create_user_request: CreateUserRequest,
            expected_status: int | HTTPStatus,
    ) -> CreateUserResponse:
        response = self.user_api.create_user(
            user_data=create_user_request,
            expected_status=expected_status,
        )
        self.created_obj.append(response)
        return response

    @allure.step("Проверка создания невалидного пользователя")
    def create_invalid_user(self,
            create_user_request: CreateUserRequest,
            expected_status: int | HTTPStatus) -> requests.Response:
        return self.user_api.create_user_raw(
            user_data=create_user_request,
            expected_status=expected_status,
        )

    @allure.step("Удаление пользователя по user_id")
    def delete_user(self,
            user_id: int,
            expected_status: int | HTTPStatus) -> requests.Response:
        return self.user_api.delete_user(
            user_id=user_id,
            expected_status=expected_status,
        )

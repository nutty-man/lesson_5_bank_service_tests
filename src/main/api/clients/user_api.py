import requests
from main.api.schemas.dto.base_model import BaseModel
from collections.abc import Callable
from requests import Response
from main.api.clients.base_api import BaseApi
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest


class UserApi(BaseApi):
    CREATE_USER_ENDPOINT = "/admin/create"
    DELETE_USER_ENDPOINT = "/admin/users/{user_id}"

    def create_user(self,
                    user_data: CreateUserRequest,
                    response_spec: Callable[[Response], None] | None = None,
                    response_model: type[BaseModel] | None = None, ) -> requests.Response:
        return self.post(
            endpoint=self.CREATE_USER_ENDPOINT,
            json_data=user_data.model_dump(mode="json"),
            response_spec=response_spec,
            response_model=response_model
        )

    def delete_user(self, user_id: int) -> requests.Response:
        endpoint = self.DELETE_USER_ENDPOINT.format(user_id=user_id)

        return self.delete(
            endpoint=endpoint,
        )

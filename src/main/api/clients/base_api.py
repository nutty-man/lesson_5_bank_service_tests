from typing import Any
from collections.abc import Callable
from requests import Response

import requests

from main.api.foundation.requester import Requester
from main.api.schemas.dto.base_model import BaseModel


class BaseApi:
    def __init__(self, requester: Requester):
        self.requester = requester

    def get(self, endpoint: str,
            headers: dict[str, str | None] | None = None,
            response_spec: Callable[[Response], None] | None = None,
            response_model: type[BaseModel] | None = None
            ) -> requests.Response:
        return self.requester.send_request(
            method="GET",
            endpoint=endpoint,
            headers=headers,
            response_spec=response_spec,
            response_model=response_model,
        )

    def post(self, endpoint: str,
             json_data: dict[str, Any] | None = None,
             headers: dict[str, str | None] | None = None,
             response_spec: Callable[[Response], None] | None = None,
             response_model: type[BaseModel] | None = None
             ) -> requests.Response:
        return self.requester.send_request(
            method="POST",
            endpoint=endpoint,
            json_data=json_data,
            headers=headers,
            response_spec=response_spec,
            response_model=response_model,
        )

    def delete(
            self,
            endpoint: str,
            headers: dict[str, str | None] | None = None,
    ) -> requests.Response:
        return self.requester.send_request(
            method="DELETE",
            endpoint=endpoint,
            headers=headers,
        )

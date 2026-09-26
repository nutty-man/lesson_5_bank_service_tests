from typing import Any

import requests

from main.api.foundation.requester import Requester


class BaseApi:
    def __init__(self, requester: Requester):
        self.requester = requester

    def get(self, endpoint: str,
            headers: dict[str, str | None] | None = None,
    ) -> requests.Response:
        return self.requester.send_request(
            method="GET",
            endpoint=endpoint,
            headers=headers,
        )

    def post(self, endpoint: str,
            json_data: dict[str, Any] | None = None,
            headers: dict[str, str | None] | None = None,
    ) -> requests.Response:
        return self.requester.send_request(
            method="POST",
            endpoint=endpoint,
            json_data=json_data,
            headers=headers,
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

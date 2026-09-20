import json
import logging
from http import HTTPStatus
from typing import Any

import allure
import requests

from main.api.config.api_config import ApiConfig
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


class Requester:
    def __init__(self, session: requests.Session, config: ApiConfig):
        self.session = session
        self.base_url = config.base_url
        self.timeout = config.timeout
        self.verify_ssl = config.verify_ssl
        self.logger = logging.getLogger(__name__)

        self.session.headers.update(RequestSpecs.base_headers())

    def send_request(
        self,
        method: str,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str | None] | None = None,
        expected_status: int | HTTPStatus = HTTPStatus.OK,
    ) -> requests.Response:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        with allure.step(f"{method.upper()} {endpoint}"):
            if json_data is not None:
                allure.attach(
                    json.dumps(json_data, ensure_ascii=False, indent=2),
                    name="Request body",
                    attachment_type=allure.attachment_type.JSON,
                )

            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )

            allure.attach(
                response.text,
                name="Response body",
                attachment_type=allure.attachment_type.JSON,
            )

        self.log_request_and_response(response)
        ResponseSpecs.validate_status(response, expected_status)
        return response

    def log_request_and_response(self, response: requests.Response) -> None:
        request = response.request
        self.logger.info(
            "%s %s -> %s",
            request.method,
            request.url,
            response.status_code,
        )

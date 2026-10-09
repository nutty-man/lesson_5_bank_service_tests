import json
import logging
from collections.abc import Callable
from requests import Response
from typing import Any

import allure
import requests

from main.api.config.api_config import ApiConfig
from main.api.schemas.dto.base_model import BaseModel
from main.api.specs.request_specs import RequestSpecs
from main.utils.logger.logger import log_request_and_response
from main.utils.logger.mask import sanitize


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
            response_spec: Callable[[Response], None] | None = None,
            response_model: type[BaseModel] | None = None,
            headers: dict[str, str | None] | None = None,
    ) -> Response | BaseModel:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        with allure.step(f"{method.upper()} {endpoint}"):
            if json_data is not None:
                allure.attach(
                    json.dumps(
                        sanitize(json_data),
                        ensure_ascii=False,
                        indent=2,
                    ),
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

            try:
                response_body = sanitize(response.json())
                response_body = json.dumps(
                    response_body,
                    ensure_ascii=False,
                    indent=2,
                )
            except ValueError:
                response_body = response.text

            allure.attach(
                response_body,
                name="Response body",
                attachment_type=allure.attachment_type.JSON,
            )

            log_request_and_response(response)

            if response_spec is not None:
                response_spec(response)

            if response_model is not None:
                return response_model.model_validate(response.json())

        return response

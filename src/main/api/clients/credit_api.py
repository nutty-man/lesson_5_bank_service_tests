from typing import Optional
from collections.abc import Callable
import requests

from main.api.clients.base_api import BaseApi
from requests import Response
from main.api.schemas.dto.base_model import BaseModel

from main.api.schemas.dto.request.credit.create_credit_request import CreateCreditRequest
from main.api.schemas.dto.request.credit.create_credit_repay_request import CreateCreditRepayRequest


class CreditApi(BaseApi):
    CREATE_CREDIT_ENDPOINT = "/credit/request"
    CREATE_CREDIT_REPAY_ENDPOINT = "/credit/repay"
    GET_CREDIT_HISTORY_ENDPOINT = "/credit/history"

    def create_credit(self, credit_data: CreateCreditRequest,
                      headers: Optional[dict] = None,
                      response_spec: Callable[[Response], None] | None = None,
                      response_model: type[BaseModel] | None = None,
                      ):
        return self.post(
            endpoint=self.CREATE_CREDIT_ENDPOINT,
            json_data=credit_data.model_dump(mode="json"),
            headers=headers,
            response_spec=response_spec,
            response_model=response_model
        )

    def create_credit_repay(self, credit_data: CreateCreditRepayRequest,
                            headers: Optional[dict] = None,
                            response_spec: Callable[[Response], None] | None = None,
                            response_model: type[BaseModel] | None = None
                            ):
        return self.post(
            endpoint=self.CREATE_CREDIT_REPAY_ENDPOINT,
            json_data=credit_data.model_dump(mode="json"),
            headers=headers,
            response_spec=response_spec,
            response_model=response_model
        )

    def get_credit_history(self, headers: Optional[dict] = None,
                           response_spec: Callable[[Response], None] | None = None,
                           response_model: type[BaseModel] | None = None
                           ):
        return self.get(
            endpoint=self.GET_CREDIT_HISTORY_ENDPOINT,
            headers=headers,
            response_spec=response_spec,
            response_model=response_model
        )

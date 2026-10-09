from typing import Optional

import requests

from main.api.clients.base_api import BaseApi
from main.api.schemas.dto.request.credit.create_credit_request import CreateCreditRequest
from main.api.schemas.dto.request.credit.create_credit_repay_request import CreateCreditRepayRequest


class CreditApi(BaseApi):
    CREATE_CREDIT_ENDPOINT = "/credit/request"
    CREATE_CREDIT_REPAY_ENDPOINT = "/credit/repay"
    GET_CREDIT_HISTORY_ENDPOINT = "/credit/history"

    def create_credit(self, credit_data: CreateCreditRequest,
                      headers: Optional[dict] = None) -> requests.Response:
        return self.post(
            endpoint=self.CREATE_CREDIT_ENDPOINT,
            json_data=credit_data.model_dump(mode="json"),
            headers=headers

        )

    def create_credit_repay(self, credit_data: CreateCreditRepayRequest,
                            headers: Optional[dict] = None) -> requests.Response:
        return self.post(
            endpoint=self.CREATE_CREDIT_REPAY_ENDPOINT,
            json_data=credit_data.model_dump(mode="json"),
            headers=headers
        )

    def get_credit_history(self, headers: Optional[dict] = None) -> requests.Response:
        return self.get(
            endpoint=self.GET_CREDIT_HISTORY_ENDPOINT,
            headers=headers
        )

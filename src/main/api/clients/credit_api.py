import requests

from main.api.clients.base_api import BaseApi
from main.api.schemas.dto.request.credit.create_credit_request import CreateCreditRequest
from main.api.schemas.dto.request.credit.create_credit_repay_request import CreateCreditRepayRequest


class CreditApi(BaseApi):
    CREATE_CREDIT_ENDPOINT = "/credit/request"
    CREATE_CREDIT_REPAY_ENDPOINT = "/credit/request"
    GET_CREDIT_HISTORY_ENDPOINT = "/credit/history"

    def create_credit_endpoint(self, credit_data: CreateCreditRequest) -> requests.Response:
        return self.post(
            endpoint=self.CREATE_CREDIT_ENDPOINT,
            json_data=credit_data.model_dump(mode="json")
        )

    def create_credit_repay_endpoint(self, credit_data: CreateCreditRepayRequest) -> requests.Response:
        return self.post(
            endpoint=self.CREATE_CREDIT_REPAY_ENDPOINT,
            json_data=credit_data.model_dump(mode="json")
        )

    def get_credit_history_endpoint(self) -> requests.Response:
        endpoint = self.GET_CREDIT_HISTORY_ENDPOINT

        return self.get(
            endpoint=endpoint
        )
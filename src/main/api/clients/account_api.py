from typing import Optional
from collections.abc import Callable
from requests import Response

from main.api.clients.base_api import BaseApi
from main.api.schemas.dto.base_model import BaseModel
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.account.account_transfer_request import AccountTransferRequest
from main.api.schemas.dto.response.account.account_transactions_response import AccountTransactionsResponse


class AccountApi(BaseApi):
    CREATE_ACCOUNT_ENDPOINT = "/account/create"
    DEPOSIT_TO_ACCOUNT_ENDPOINT = "/account/deposit"
    TRANSFER_TO_ACCOUNT_ENDPOINT = "/account/transfer"
    TRANSACTIONS_HISTORY_ENDPOINT = "/account/transactions/{id}"

    def create_account(self,
                       response_spec: Callable[[Response], None] | None = None,
                       response_model: type[BaseModel] | None = None,
                       ):
        return self.post(
            endpoint=self.CREATE_ACCOUNT_ENDPOINT,
            response_spec=response_spec,
            response_model=response_model,
        )

    def deposit_to_account(self,
                           deposit_data: AccountDepositRequest,
                           headers: Optional[dict] = None,
                           response_spec: Callable[[Response], None] | None = None,
                           ):
        return self.post(
            endpoint=self.DEPOSIT_TO_ACCOUNT_ENDPOINT,
            json_data=deposit_data.model_dump(mode="json"),
            headers=headers,
            response_spec=response_spec
        )

    def transfer_to_account(
            self,
            transfer_data: AccountTransferRequest,
            headers: Optional[dict] = None,
            response_spec: Callable[[Response], None] | None = None,
    ):
        return self.post(
            endpoint=self.TRANSFER_TO_ACCOUNT_ENDPOINT,
            json_data=transfer_data.model_dump(mode="json"),
            headers=headers,
            response_spec=response_spec,
        )

    def get_transactions_history(self, account_id,
                                 headers: Optional[dict] = None,
                                 response_spec: Callable[[Response], None] | None = None,
                                 response_model: type[BaseModel] | None = None,):
        return self.get(
            endpoint=self.TRANSACTIONS_HISTORY_ENDPOINT.format(id=account_id),
            headers=headers,
            response_spec=response_spec,
            response_model=response_model
        )

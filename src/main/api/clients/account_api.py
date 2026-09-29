from typing import Optional

from main.api.clients.base_api import BaseApi
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.account.account_transfer_request import AccountTransferRequest


class AccountApi(BaseApi):
    CREATE_ACCOUNT_ENDPOINT = "/account/create"
    DEPOSIT_TO_ACCOUNT_ENDPOINT = "/account/deposit"
    TRANSFER_TO_ACCOUNT_ENDPOINT = "/account/transfer"
    TRANSACTIONS_HISTORY_ENDPOINT = "/account/transactions/{id}"

    def create_account(self):
        return self.post(
            endpoint=self.CREATE_ACCOUNT_ENDPOINT
        )

    def deposit_to_account(self,
                           deposit_data: AccountDepositRequest,
                           headers: Optional[dict] = None):
        return self.post(
            endpoint=self.DEPOSIT_TO_ACCOUNT_ENDPOINT,
            json_data=deposit_data.model_dump(mode="json"),
            headers=headers
        )

    def transfer_to_account(self,
                            deposit_data: AccountTransferRequest,
        headers: Optional[dict] = None):
        return self.post(
            endpoint=self.TRANSFER_TO_ACCOUNT_ENDPOINT,
            json_data=deposit_data.model_dump(mode="json"),
            headers=headers
        )

    def get_transactions_history(self, account_id, headers: Optional[dict] = None):
        return self.get(endpoint=self.TRANSACTIONS_HISTORY_ENDPOINT.format(id=account_id),
                        headers=headers)

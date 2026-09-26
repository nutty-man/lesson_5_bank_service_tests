from main.api.clients.base_api import BaseApi
from main.api.schemas.dto.request.account.account_deposit_request import AccountDepositRequest
from main.api.schemas.dto.request.account.account_transfer_request import AccountTransferRequest


class AccountApi(BaseApi):
    CREATE_ACCOUNT_ENDPOINT = "/account/create"
    DEPOSIT_TO_ACCOUNT_ENDPOINT = "/account/deposit"
    TRANSFER_TO_ACCOUNT_ENDPOINT = "/account/transfer"

    def create_account(self):
        return self.post(
            endpoint=self.CREATE_ACCOUNT_ENDPOINT
        )

    def deposit_to_account(self, deposit_data: AccountDepositRequest):
        return self.post(
            endpoint=self.DEPOSIT_TO_ACCOUNT_ENDPOINT,
            json_data=deposit_data.model_dump(mode="json")
        )

    def transfer_to_account(self, deposit_data: AccountTransferRequest):
        return self.post(
            endpoint=self.TRANSFER_TO_ACCOUNT_ENDPOINT,
            json_data=deposit_data.model_dump(mode="json")
        )

    def get_transactions_history(self, account_id):
        return self.get(endpoint=self.TRANSFER_TO_ACCOUNT_ENDPOINT.format(id=account_id))


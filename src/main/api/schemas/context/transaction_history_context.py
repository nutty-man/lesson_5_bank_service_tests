from dataclasses import dataclass

from main.api.schemas.dto.response.account.create_account_response import CreateAccountResponse


@dataclass
class TransactionHistoryContext:
    account: CreateAccountResponse
    expected_balance: float
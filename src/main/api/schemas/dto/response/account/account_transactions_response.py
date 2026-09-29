from typing import List, Optional

from main.api.schemas.dto.base_model import BaseModel


class Transactions(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int]
    toAccountId: int
    createdAt: str

class AccountTransactionsResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: List[Transactions]
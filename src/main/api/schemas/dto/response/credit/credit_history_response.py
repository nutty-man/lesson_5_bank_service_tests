from typing import List

from main.api.schemas.dto.base_model import BaseModel


class Credits(BaseModel):
    creditId: int
    accountId: int
    amount: float
    termMonths: int
    balance: float
    createdAt: str


class CreditHistoryRequest(BaseModel):
    userId: int
    credits: List[Credits]
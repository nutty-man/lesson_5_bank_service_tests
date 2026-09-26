from main.api.schemas.dto.base_model import BaseModel


class AccountTransferRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: float
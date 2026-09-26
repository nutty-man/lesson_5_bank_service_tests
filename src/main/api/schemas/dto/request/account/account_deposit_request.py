from main.api.schemas.dto.base_model import BaseModel

class AccountDepositRequest(BaseModel):
    accountId: int
    amount: float
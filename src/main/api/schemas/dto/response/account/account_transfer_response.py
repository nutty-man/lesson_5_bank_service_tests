from main.api.schemas.dto.base_model import BaseModel


class AccountTransferResponse(BaseModel):
    fromAccountId: int
    toAccountId: int
    fromAccountIdBalance: float
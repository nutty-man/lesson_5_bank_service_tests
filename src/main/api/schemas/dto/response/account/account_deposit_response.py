from main.api.schemas.dto.base_model import BaseModel


class AccountDepositResponse(BaseModel):
    id: int
    balance: float
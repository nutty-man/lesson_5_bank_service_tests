from main.api.schemas.dto.base_model import BaseModel


class CreateCreditRepayRequest(BaseModel):
    creditId: int
    accountId: int
    amount: int
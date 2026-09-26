from main.api.schemas.dto.base_model import BaseModel


class CreateCreditRepayResponse(BaseModel):
    creditId: int
    amountDeposited: int

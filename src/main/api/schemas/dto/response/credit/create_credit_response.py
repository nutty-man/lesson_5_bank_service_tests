from main.api.schemas.dto.base_model import BaseModel


class CreateCreditResponse(BaseModel):
  accountId: int
  amount: float
  termMonths: int
  balance: float
  creditId: int

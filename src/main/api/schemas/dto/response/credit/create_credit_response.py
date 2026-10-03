from main.api.schemas.dto.base_model import BaseModel


class CreateCreditResponse(BaseModel):
  id: int
  amount: float
  termMonths: int
  balance: float
  creditId: int

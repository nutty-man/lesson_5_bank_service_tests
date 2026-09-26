from main.api.schemas.dto.base_model import BaseModel


class CreateCreditRequest(BaseModel):
  accountId: int
  amount: int
  termMonths: int

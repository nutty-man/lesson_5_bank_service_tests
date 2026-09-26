from main.api.schemas.dto.base_model import BaseModel


class CreateAccountResponse(BaseModel):
    id: int
    number: str
    balance: float

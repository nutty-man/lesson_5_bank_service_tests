from typing import Annotated

from main.api.data_generators.creation_rule import RangeCreationRule
from main.api.schemas.dto.base_model import BaseModel


class CreateCreditRepayRequest(BaseModel):
    creditId: int
    accountId: int
    amount: Annotated[
        float,
        RangeCreationRule(min_value=5000, max_value=15000)
    ]
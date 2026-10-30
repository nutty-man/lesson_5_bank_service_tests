from typing import Annotated

from main.api.data_generators.creation_rule import RangeCreationRule
from main.api.schemas.dto.base_model import BaseModel

class AccountDepositRequest(BaseModel):
    accountId: int
    amount: Annotated[
        float,
        RangeCreationRule(min_value=1000, max_value=9000)
    ]
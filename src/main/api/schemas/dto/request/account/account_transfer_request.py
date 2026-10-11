from typing import Annotated

from main.api.data_generators.creation_rule import RangeCreationRule
from main.api.schemas.dto.base_model import BaseModel


class AccountTransferRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: Annotated[
        float,
        RangeCreationRule(min_value=500, max_value=10000)
    ]

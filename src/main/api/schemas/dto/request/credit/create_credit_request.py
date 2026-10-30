from typing import Annotated

from main.api.data_generators.creation_rule import RangeCreationRule
from main.api.schemas.dto.base_model import BaseModel


class CreateCreditRequest(BaseModel):
    accountId: int
    amount: Annotated[float,
        RangeCreationRule(min_value=5000, max_value=15000)
    ]
    termMonths: Annotated[int,
        RangeCreationRule(min_value=1, max_value=60)
    ]

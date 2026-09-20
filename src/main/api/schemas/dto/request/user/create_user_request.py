from typing import Annotated

from main.api.data_generators.creation_rule import CreationRule
from main.api.schemas.dto.base_model import BaseModel
from main.utils.enums.role import Role


class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationRule(regex=r"^[A-Za-z0-9]{3,15}$")]
    password: Annotated[str, CreationRule(regex=r"^[A-Z]{3}[a-z][0-9]{2}[!$_]{4}$")]
    role: Role = Role.USER

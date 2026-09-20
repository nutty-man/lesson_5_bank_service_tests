from main.api.schemas.dto.base_model import BaseModel
from main.utils.enums.role import Role


class User(BaseModel):
    username: str
    role: Role

class CreateUserResponse(BaseModel):
    id: int
    username: str
    role: Role

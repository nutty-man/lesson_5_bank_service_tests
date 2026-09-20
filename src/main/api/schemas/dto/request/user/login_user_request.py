from main.api.schemas.dto.base_model import BaseModel


class LoginUserRequest(BaseModel):
    username: str
    password: str

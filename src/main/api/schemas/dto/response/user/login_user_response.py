from main.api.schemas.dto.base_model import BaseModel
from main.api.schemas.dto.response.user.create_user_response import User


class LoginUserResponse(BaseModel):
    token: str
    user: User


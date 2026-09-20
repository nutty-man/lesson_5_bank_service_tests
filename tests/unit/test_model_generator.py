import re

from main.api.data_generators.model_generator import RandomModelGenerator
from main.api.schemas.dto.request.user.create_user_request import CreateUserRequest
from main.utils.enums.role import Role


def test_generator_populates_model_fields() -> None:
    model = RandomModelGenerator.generate(CreateUserRequest, role=Role.USER)

    assert re.fullmatch(r"[A-Za-z0-9]{3,15}", model.username)
    assert re.fullmatch(r"[A-Z]{3}[a-z][0-9]{2}[!$_]{4}", model.password)
    assert model.role is Role.USER

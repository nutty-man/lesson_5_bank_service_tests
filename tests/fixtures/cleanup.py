import logging
from typing import List, Any

from main.api.classes.api_manager import ApiManager
from main.api.schemas.dto.response.user.create_user_response import CreateUserResponse


def clean_user(objects: List[Any], api_manager: ApiManager):
    for u in objects:
        if isinstance(u, CreateUserResponse):
            api_manager.admin_steps.delete_user(u.id)
        else:
            # logging.warning(
            #     f"Ошибка удаления пользователя по айди = {getattr(u, 'id', None)}"
            # )
            logging.warning(
                f"Не удалось удалить объект: "
                f"type={type(u)}, value={u}, id={getattr(u, 'id', None)}"
            )

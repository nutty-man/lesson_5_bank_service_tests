import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from sqlalchemy import URL, make_url

import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "environments.yaml"


@dataclass
class ApiConfig:
    base_url: str
    username: str
    password: str
    timeout: int = 10
    verify_ssl: bool = True


def load_config(environment: str = "local") -> ApiConfig:
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        config_data = yaml.safe_load(config_file)

    try:
        environment_config = config_data[environment]
    except KeyError as error:
        raise ValueError(f"Unknown environment: {environment}") from error

    admin_login = os.getenv("ADMIN_LOGIN")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_login or not admin_password:
        raise ValueError(
            "Не заданы параметры ADMIN_LOGIN и ADMIN_PASSWORD"
        )

    return ApiConfig(
        base_url=environment_config["api"]["base_url"],
        username=admin_login,
        password=admin_password,
        timeout=environment_config["timeout"],
        verify_ssl=environment_config["verify_ssl"],
    )

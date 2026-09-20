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
    timeout: int = 10
    verify_ssl: bool = True


def load_config(environment: str = "local") -> ApiConfig:
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        config_data = yaml.safe_load(config_file)

    try:
        environment_config = config_data[environment]
    except KeyError as error:
        raise ValueError(f"Unknown environment: {environment}") from error

    return ApiConfig(
        base_url=environment_config["api"]["base_url"],
        timeout=environment_config["timeout"],
        verify_ssl=environment_config["verify_ssl"],
    )

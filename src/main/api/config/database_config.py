from dataclasses import dataclass
from pathlib import Path
import os

from sqlalchemy.engine import URL, make_url
import yaml


CONFIG_PATH = Path(__file__).resolve().parent / "environments.yaml"


@dataclass
class DatabaseConfig:
    driver: str
    host: str
    port: int
    name: str


def load_database_config(environment: str = "local") -> DatabaseConfig:
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        config_data = yaml.safe_load(config_file)

    database_config = config_data[environment]["database"]

    return DatabaseConfig(
        driver=database_config["driver"],
        host=database_config["host"],
        port=database_config["port"],
        name=database_config["name"],
    )

def build_database_url(config: DatabaseConfig) -> URL:
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return make_url(database_url)

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if not db_user or not db_password:
        raise ValueError(
            "Не заданы параметры DB_USER и DB_PASSWORD"
        )

    return URL.create(
        drivername=config.driver,
        username=db_user,
        password=db_password,
        host=config.host,
        port=config.port,
        database=config.name,
    )

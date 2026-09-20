from main.api.config.api_config import CONFIG_PATH, load_config
from main.api.config.database_config import load_database_config


def test_is_local_config_loaded_from_yaml() -> None:
    config = load_config("local")

    assert CONFIG_PATH.name == "environments.yaml"
    assert config.base_url == "http://localhost:4111/api"
    assert config.timeout == 10
    assert config.verify_ssl is False

def test_is_db_config_loaded_from_yaml() -> None:
    config = load_database_config('local')

    assert config.name == "symfony_db"
    assert config.port == 5432

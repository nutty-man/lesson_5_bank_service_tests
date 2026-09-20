import os

import pytest
from dotenv import load_dotenv

from main.api.classes.api_manager import ApiManager
from main.api.config.api_config import load_config, ApiConfig
from tests.fixtures.cleanup import clean_user

pytest_plugins = [
    "tests.fixtures.user",
    "tests.fixtures.api",
    "tests.fixtures.account",
    "tests.fixtures.object",
    "tests.fixtures.cleanup",
    "tests.fixtures.db",
]

load_dotenv()  # загружает переменные из файлика .env

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=os.getenv("TEST_ENV", "local"),
        help="Environment key from environments.yaml (default: local)",
    )

@pytest.fixture(scope="session")
def config() -> ApiConfig:
    return load_config()

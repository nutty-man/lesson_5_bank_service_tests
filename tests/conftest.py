import os

import pytest
from dotenv import load_dotenv

from main.api.config.api_config import load_config, ApiConfig
from main.api.config.database_config import DatabaseConfig, load_database_config

pytest_plugins = [
    "tests.fixtures.user",
    "tests.fixtures.api",
    "tests.fixtures.account",
    "tests.fixtures.credit",
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
def config(pytestconfig) -> ApiConfig:
    environment = pytestconfig.getoption("--env")
    return load_config(environment)

@pytest.fixture(scope="session")
def database_config(pytestconfig) -> DatabaseConfig:
    environment = pytestconfig.getoption("--env")
    return load_database_config(environment)

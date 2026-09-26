import pytest

from main.api.config.database_config import DatabaseConfig
from main.db.session import create_session_factory


@pytest.fixture(scope="session")
def db_engine_and_factory(database_config: DatabaseConfig):
    engine, session_factory = create_session_factory(database_config)
    yield engine, session_factory
    engine.dispose()


@pytest.fixture
def db_session(db_engine_and_factory):
    engine, session_factory = db_engine_and_factory
    connection = engine.connect()
    transaction = connection.begin()
    session = session_factory(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

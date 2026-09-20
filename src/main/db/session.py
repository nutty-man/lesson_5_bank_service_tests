from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main.api.config.database_config import DatabaseConfig, build_database_url


def create_session_factory(config: DatabaseConfig):
    database_url = build_database_url(config)
    engine = create_engine(database_url)
    return engine, sessionmaker(bind=engine)
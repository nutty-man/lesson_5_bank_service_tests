import pytest
from sqlalchemy.orm import Session

from main.db.repositories.account_repository import AccountRepository


@pytest.fixture
def account_repository(db_session: Session):
    return AccountRepository(db_session)
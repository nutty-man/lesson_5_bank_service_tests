from sqlalchemy.orm import Session

from main.db.models.account_table import AccountTable


class AccountRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_account_by_id(self, account_id: int) -> AccountTable | None:
        return self.session.get(AccountTable, account_id)

    def delete(self, account_id: int) -> None:
        account = self.session.get(AccountTable, account_id)

        if account:
            self.session.delete(account)
            self.session.commit()

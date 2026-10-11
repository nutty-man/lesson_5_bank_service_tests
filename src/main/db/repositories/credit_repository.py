from sqlalchemy.orm import Session

from main.db.models.credit_table import CreditTable


class CreditRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_credit_by_id(self, credit_id: int) -> CreditTable | None:
        return self.session.get(CreditTable, credit_id)

    def delete(self, credit_id: int) -> None:
        credit = self.session.get(CreditTable, credit_id)

        if credit:
            self.session.delete(credit)
            self.session.commit()

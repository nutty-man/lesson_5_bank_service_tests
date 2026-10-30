from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from sqlalchemy import DateTime

from main.db.base import Base


class CreditTable(Base):
    __tablename__ = "credit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    term_months: Mapped[int] = mapped_column(String, unique=True, nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self):
        return (f'<Credit(id={self.id}, account_id={self.account_id}, amount={self.amount},'
                f'term_months={self.term_months}, balance={self.balance}, created_at={self.created_at}>')

from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column

from main.db.base import Base

class AccountTable(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<Account(id={self.id}, user_id={self.user_id}, number={self.number}, balance={self.balance}>'

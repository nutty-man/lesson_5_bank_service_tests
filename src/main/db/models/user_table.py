from datetime import datetime

from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped, mapped_column
from main.db.base import Base
from sqlalchemy import Integer, String


class UserTable(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, role={self.role}, deleted_at={self.deleted_at}>'

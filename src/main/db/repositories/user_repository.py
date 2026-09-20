from sqlalchemy.orm import Session

from main.db.models.user_table import UserTable as User
from main.utils.enums.role import Role


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> User | None:

        return (
            self.db
            .query(User)
            .filter_by(username=username)
            .first()
        )

    def create(self, username: str, password: str, role: Role
    ) -> User:

        user = User(
            username=username,
            password=password,
            role=role
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

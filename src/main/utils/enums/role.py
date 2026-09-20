from enum import StrEnum


class Role(StrEnum):
    USER = "ROLE_USER"
    CREDIT_SECRET = "ROLE_CREDIT_SECRET"
    ADMIN = "ROLE_ADMIN"
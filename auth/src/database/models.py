from datetime import datetime

from popug_legacy_sdk.schemas import UserRoles
from sqlalchemy import (
    DateTime,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRoles] = mapped_column(
        nullable=False,
        default=UserRoles.CUSTOMER,
        server_default=text(f"'{UserRoles.CUSTOMER.value}'"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        server_default=text("(now() at time zone 'utc')"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        server_default=text("(now() at time zone 'utc')"),
        onupdate=datetime.utcnow,
    )

from helpers.sqlalchemy.base_model import Base
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.db.enums.user import UserStatus


class User(Base):
    __tablename__ = 'users'
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.NOT_REGISTERED, nullable=False)

from decimal import Decimal
from typing import TYPE_CHECKING

from helpers.sqlalchemy.base_model import Base
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enums.user import UserStatus

if TYPE_CHECKING:
    from src.db.models.user_favorite import UserFavorite


class User(Base):
    __tablename__ = 'users'
    first_name: Mapped[str]
    last_name: Mapped[str]
    score: Mapped[Decimal] = mapped_column(default=5.0)
    email: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.NOT_VERIFIED, nullable=False)

    favorites: Mapped['UserFavorite'] = relationship('UserFavorite', back_populates='user')

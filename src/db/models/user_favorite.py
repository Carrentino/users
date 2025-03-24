from typing import TYPE_CHECKING
from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.db.models.user import User


class UserFavorite(Base):
    __tablename__ = "user_favorites"
    __table_args__ = (Index('ix_user_favorite_user_id', 'user_id'),)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    car_id: Mapped[UUID] = mapped_column(nullable=False)

    user: Mapped['User'] = relationship('User', back_populates="favorites")

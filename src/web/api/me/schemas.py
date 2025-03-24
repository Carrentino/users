from uuid import UUID

from pydantic import BaseModel

from src.db.enums.user import UserStatus


class UpdateFavoritesReq(BaseModel):
    car_id: UUID


class UserProfile(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str | None = None
    status: UserStatus
    balance: int | None = None
    reviews: list

    class Config:
        from_attributes = True


class FavoritesFilters(BaseModel):
    limit: int = 30
    offset: int = 0

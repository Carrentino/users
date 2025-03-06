from uuid import UUID

from pydantic import BaseModel

from src.db.enums.user import UserStatus


class UpdateFavoritesReq(BaseModel):
    car_id: UUID


class UserProfile(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    status: UserStatus

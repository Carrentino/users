from uuid import UUID

from pydantic import BaseModel


class UpdateFavoritesReq(BaseModel):
    car_id: UUID

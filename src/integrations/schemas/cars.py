from datetime import datetime
from decimal import Decimal
from uuid import UUID

from helpers.models.response import PaginatedResponse
from pydantic import BaseModel


class BrandSchema(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime


class CarModelSchema(BaseModel):
    id: UUID
    title: str
    body: str
    fuel_consumption: Decimal
    engine_capacity: Decimal
    drive: str
    gearbox: str
    fuel: str
    hp: int
    created_at: datetime
    updated_at: datetime
    brand: BrandSchema


class CarSchema(BaseModel):
    id: UUID
    color: str
    score: Decimal
    price: int
    owner_id: UUID
    latitude: str
    longitude: str
    date_from: datetime | None
    date_to: datetime | None
    status: str
    created_at: datetime
    updated_at: datetime
    car_model: CarModelSchema


class CarPaginatedResponse(PaginatedResponse):
    data: list[CarSchema]

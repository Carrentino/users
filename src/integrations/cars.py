from uuid import UUID

from helpers.clients.http_client import BaseApiClient
from httpx import HTTPError

from src.integrations.schemas.cars import CarPaginatedResponse
from src.settings import get_settings


class CarsClient(BaseApiClient):
    _base_url = get_settings().cars_url

    async def get_cars(self, ids: list[UUID], limit: int = 30, offset: int = 0) -> CarPaginatedResponse:
        url = f'{self._base_url.join('api/listings/')}?limit={limit}&offset={offset}'
        for car_id in ids:
            url += f'&car__id={car_id}'
        response = await self.get(url)
        try:
            response.raise_for_status()
        except HTTPError:
            return CarPaginatedResponse(data=[])
        return CarPaginatedResponse.model_validate_json(response.json())

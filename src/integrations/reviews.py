from urllib.error import HTTPError
from urllib.parse import urljoin
from uuid import UUID

from helpers.clients.http_client import BaseApiClient

from src.settings import get_settings


class ReviewsClient(BaseApiClient):
    _base_url = get_settings().reviews_url

    async def get_reviews(self, user_id: UUID, token: str | None = None) -> list:
        if token is not None:
            self.headers['X-Auth-Token'] = token
        response = await self.get(urljoin(self._base_url, f"users/{user_id}/?limit=3&sort=popularity"))
        try:
            response.raise_for_status()
        except HTTPError:
            return []
        return response.json()['data']

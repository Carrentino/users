from uuid import UUID

from helpers.models.user import UserContext

from src.db.models.user_favorite import UserFavorite
from src.integrations.cars import CarsClient
from src.integrations.schemas.cars import CarPaginatedResponse
from src.repositories.user_favorite import UserFavoriteRepository
from src.web.api.me.schemas import FavoritesFilters


class UserFavoriteService:
    def __init__(self, user_favorite_repository: UserFavoriteRepository, cars_client: CarsClient):
        self.user_favorite_repository = user_favorite_repository
        self.cars_client = cars_client

    async def update_favorite(self, user: UserContext, car_id: UUID) -> None:
        favorite = await self.user_favorite_repository.get_one_by(user_id=user.user_id, car_id=car_id)
        if favorite is None:
            user_favorite = UserFavorite(car_id=car_id, user_id=UUID(user.user_id))
            await self.user_favorite_repository.create(user_favorite)
            return
        await self.user_favorite_repository.delete(favorite.id)

    async def get_favorites(self, user_id: UUID, filters: FavoritesFilters) -> CarPaginatedResponse:
        favorites = await self.user_favorite_repository.get_list(user_id=user_id)
        return await self.cars_client.get_cars([item.car_id for item in favorites], filters.limit, filters.offset)

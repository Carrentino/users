from uuid import UUID

from helpers.models.user import UserContext

from src.db.models.user_favorite import UserFavorite
from src.repositories.user_favorite import UserFavoriteRepository


class UserFavoriteService:
    def __init__(self, user_favorite_repository: UserFavoriteRepository):
        self.user_favorite_repository = user_favorite_repository

    async def update_favorite(self, user: UserContext, car_id: UUID) -> None:
        favorite = await self.user_favorite_repository.get_one_by(user_id=user.user_id, car_id=car_id)
        if favorite is None:
            user_favorite = UserFavorite(car_id=car_id, user_id=user.user_id)
            await self.user_favorite_repository.create(user_favorite)
            return
        await self.user_favorite_repository.delete(favorite.id)

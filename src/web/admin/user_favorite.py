from sqladmin import ModelView

from src.db.models.user_favorite import UserFavorite


class UserFavoriteAdmin(ModelView, model=UserFavorite):
    column_list = [UserFavorite.user_id, UserFavorite.car_id]  # noqa: RUF012

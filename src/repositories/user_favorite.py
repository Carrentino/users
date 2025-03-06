from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.user_favorite import UserFavorite


class UserFavoriteRepository(ISqlAlchemyRepository[UserFavorite]):
    _model = UserFavorite

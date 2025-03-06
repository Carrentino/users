from uuid import uuid4

import factory

from src.db.models.user_favorite import UserFavorite
from tests.factories.base import BaseSqlAlchemyFactory


class UserFavoriteFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = UserFavorite

    user = factory.SubFactory('tests.factories.user.UserFactory')
    car_id = factory.LazyAttribute(lambda _: str(uuid4()))

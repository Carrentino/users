import factory

from src.db.enums.user import UserStatus
from src.db.models.user import User
from tests.factories.base import BaseSqlAlchemyFactory


class UserFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    password = factory.Faker("password")
    status = factory.Iterator(UserStatus)

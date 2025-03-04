import random
import string

from helpers.redis.client import RedisClient
from sqlalchemy.exc import IntegrityError

from src.db.models.user import User
from src.errors.service import UserAlreadyExistsError
from src.integrations.notifications import NotificationsClient
from src.repositories.user_repository import UserRepository
from src.settings import get_settings
from src.web.api.users.schemas import UserRegistrationReq


class UserService:
    def __init__(self, user_repository: UserRepository, notifications_client: NotificationsClient) -> None:
        self.user_repository = user_repository
        self.notifications_client = notifications_client

    async def registration(self, req_data: UserRegistrationReq) -> None:
        req_data.password = await self.user_repository.hash_password(req_data.password)
        user = User(**req_data.model_dump())
        try:
            await self.user_repository.create(user)
        except IntegrityError:
            raise UserAlreadyExistsError from None

    def generate_code(self):
        return ''.join(random.choices(string.digits, k=6))

    async def send_email_code(self, user: User) -> None:
        code = self.generate_code()
        async with RedisClient(get_settings().redis_url) as rc:
            await rc.set(str(user.id), code, 300)
        await self.notifications_client.send_email_code(user.email, code)

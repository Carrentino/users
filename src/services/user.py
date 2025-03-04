import random
import string
from datetime import datetime, timedelta
from uuid import UUID

from helpers.enums.auth import TokenType
from helpers.jwt import encode_jwt
from helpers.redis_client.client import RedisClient
from sqlalchemy.exc import IntegrityError

from src.db.enums.user import UserStatus
from src.db.models.user import User
from src.errors.service import UserAlreadyExistsError, UserNotFoundError, InvalidUserStatusError, InvalidCodeError
from src.integrations.notifications import NotificationsClient
from src.repositories.user_repository import UserRepository
from src.settings import get_settings
from src.web.api.users.schemas import UserRegistrationReq, TokenResponse


class UserService:
    def __init__(self, user_repository: UserRepository, notifications_client: NotificationsClient) -> None:
        self.user_repository = user_repository
        self.notifications_client = notifications_client

    @staticmethod
    async def generate_code():
        return ''.join(random.choices(string.digits, k=6))

    async def registration(self, req_data: UserRegistrationReq) -> None:
        req_data.password = await self.user_repository.hash_password(req_data.password)
        user = User(**req_data.model_dump())
        try:
            await self.user_repository.create(user)
        except IntegrityError:
            raise UserAlreadyExistsError from None
        await self.send_email_code(user)

    async def send_email_code(self, user: User) -> None:
        code = await self.generate_code()
        async with RedisClient(get_settings().redis_url) as rc:
            await rc.set(str(user.id), code, 300)
        await self.notifications_client.send_email_code(user.email, code)

    async def verify_code(self, user_id: UUID, code: str) -> TokenResponse:
        user = await self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundError
        if user.status != UserStatus.NOT_REGISTERED:
            raise InvalidUserStatusError
        async with RedisClient(get_settings().redis_url) as rc:
            saved_code = await rc.get(user.id)
        if saved_code is None or saved_code != code:
            raise InvalidCodeError
        await self.user_repository.update(user.id, status=UserStatus.NOT_VERIFIED)
        return await self.create_tokens(user)

    @staticmethod
    async def create_tokens(user: User) -> TokenResponse:
        now = datetime.now()

        access_payload = {
            "sub": str(user.id),
            "status": user.status,
            "type": TokenType.ACCESS,
            "exp": now + timedelta(days=get_settings().auth_settings.access_lifetime),
        }

        refresh_payload = {
            "sub": str(user.id),
            "type": TokenType.REFRESH,
            "exp": now + timedelta(days=get_settings().auth_settings.refresh_lifetime),
        }
        return TokenResponse(
            access_token=encode_jwt(
                get_settings().auth_settings.secret_key.get_secret_value(),
                access_payload,
                get_settings().auth_settings.algorithm,
            ),
            refresh_token=encode_jwt(
                get_settings().auth_settings.secret_key.get_secret_value(),
                refresh_payload,
                get_settings().auth_settings.algorithm,
            ),
        )

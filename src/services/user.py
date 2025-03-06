import random
import string
from datetime import datetime, timedelta
from typing import ClassVar
from uuid import UUID

from helpers.enums.auth import TokenType
from helpers.jwt import encode_jwt
from helpers.redis_client.client import RedisClient
from sqlalchemy.exc import IntegrityError

from src.db.enums.user import UserStatus
from src.db.models.user import User
from src.errors.service import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidUserStatusError,
    InvalidCodeError,
    WrongPasswordError,
)
from src.integrations.notifications import NotificationsClient
from src.integrations.payment import PaymentClient
from src.repositories.user import UserRepository
from src.settings import get_settings
from src.web.api.me.schemas import UserProfile
from src.web.api.users.schemas import UserRegistrationReq, TokenResponse


class UserService:
    AVAILABLE_USER_STATUSES: ClassVar = [UserStatus.NOT_VERIFIED, UserStatus.VERIFIED, UserStatus.SUSPECTED]

    def __init__(
        self, user_repository: UserRepository, notifications_client: NotificationsClient, payment_client: PaymentClient
    ) -> None:
        self.user_repository = user_repository
        self.notifications_client = notifications_client
        self.payment_client = payment_client

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
            "user_id": str(user.id),
            "status": user.status,
            "type": TokenType.ACCESS,
            "exp": now + timedelta(days=get_settings().auth_settings.access_lifetime),
        }

        refresh_payload = {
            "user_id": str(user.id),
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

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.user_repository.get_one_by(email=email)
        if user is None:
            raise UserNotFoundError
        if user.status not in self.AVAILABLE_USER_STATUSES:
            raise InvalidUserStatusError
        if not await self.user_repository.verify_password(password, user.password):
            raise WrongPasswordError
        return await self.create_tokens(user)

    async def get_user(self, user_id: UUID) -> UserProfile:
        user = await self.user_repository.get(user_id)
        async with RedisClient(get_settings().redis_url, db=get_settings().balance_db) as rc:
            balance = await rc.get(str(user.id))
        if balance is None:
            balance = await self.payment_client.get_user_balance(user_id)
        async with RedisClient(get_settings().redis_url, db=get_settings().balance_db) as rc:
            await rc.set(str(user.id), balance, 600)
        return UserProfile(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            status=user.status,
            balance=balance,
        )

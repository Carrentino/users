import random
import string
from datetime import datetime, timedelta
from decimal import Decimal
from typing import ClassVar
from uuid import UUID

from helpers.enums.auth import TokenType
from helpers.jwt import encode_jwt
from helpers.redis_client.client import RedisClient
from sqlalchemy.exc import IntegrityError

from src.db.enums.user import UserStatus
from src.db.models.user import User
from src.errors.service import (
    UserNotFoundError,
    InvalidUserStatusError,
    InvalidCodeError,
    WrongPasswordError,
    UserAlreadyExistsError,
)
from src.integrations.notifications import NotificationsClient
from src.integrations.payment import PaymentClient
from src.integrations.reviews import ReviewsClient
from src.integrations.schemas.notifications import EmailNotification
from src.repositories.user import UserRepository
from src.settings import get_settings
from src.web.api.me.schemas import UserProfile
from src.web.api.users.schemas import (
    UserRegistrationReq,
    TokenResponse,
    UserFI,
    UsersFilterId,
    VerifyTokenReq,
    ChangePasswordTokenReq,
)


class UserService:
    AVAILABLE_USER_STATUSES: ClassVar = [UserStatus.NOT_VERIFIED, UserStatus.VERIFIED, UserStatus.SUSPECTED]

    def __init__(
        self,
        user_repository: UserRepository,
        notifications_client: NotificationsClient,
        payment_client: PaymentClient,
        reviews_client: ReviewsClient,
    ) -> None:
        self.user_repository = user_repository
        self.notifications_client = notifications_client
        self.payment_client = payment_client
        self.reviews_client = reviews_client

    @staticmethod
    async def generate_code():
        return ''.join(random.choices(string.digits, k=6))

    async def registration(self, req_data: UserRegistrationReq) -> None:
        await self.send_email_code(req_data.email, 'Регистрация Carrentino')

    async def send_email_code(self, email: str, title: str) -> None:
        code = await self.generate_code()
        async with RedisClient(get_settings().redis.url, db=get_settings().redis.email_code_db) as rc:
            await rc.set(email, code, 300)
        message = EmailNotification(
            email=email,
            title=title,
            body=code,
        )
        await self.notifications_client.send_email_notification(message)

    async def verify_code(self, user: VerifyTokenReq) -> TokenResponse:
        created_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            password=await self.user_repository.hash_password(user.password),
        )
        async with RedisClient(get_settings().redis.url, db=get_settings().redis.email_code_db) as rc:
            saved_code = await rc.get(user.email)
        if saved_code is None or saved_code != user.code:
            raise InvalidCodeError
        try:
            await self.user_repository.create(created_user)
        except IntegrityError:
            raise UserAlreadyExistsError from None
        return await self.create_tokens(created_user)

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

    async def get_user(self, user_id: UUID, current_user_id: UUID, token: str | None = None) -> UserProfile:
        user = await self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundError
        reviews = await self.reviews_client.get_reviews(user_id, token)
        if user_id != current_user_id:
            return UserProfile(
                id=user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                status=user.status,
                reviews=reviews,
            )
        async with RedisClient(get_settings().redis.url, db=get_settings().redis.balance_db) as rc:
            balance = await rc.get(str(user.id))
        if balance is None:
            balance = await self.payment_client.get_user_balance(user_id)
        async with RedisClient(get_settings().redis.url, db=get_settings().redis.balance_db) as rc:
            await rc.set(str(user.id), balance)

        return UserProfile(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            status=user.status,
            balance=balance,
            reviews=reviews,
        )

    async def update_balance(self, user_id: UUID, balance: Decimal) -> None:
        user = await self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundError
        if user.status not in self.AVAILABLE_USER_STATUSES:
            raise InvalidUserStatusError
        async with RedisClient(get_settings().redis.url, db=get_settings().redis.balance_db) as rc:
            await rc.set(str(user_id), str(balance))

    async def get_users_by_ids(self, filters: UsersFilterId) -> list[UserFI]:
        result = []
        if filters is None:
            return result
        users = await self.user_repository.get_list(filters.user__id)
        for user in users:
            result.append(UserFI.model_validate(user))
        return result

    async def send_code_to_change_password(self, email: str) -> None:
        user = await self.user_repository.get_one_by(email=email)
        if user is None:
            raise UserNotFoundError
        await self.send_email_code(email, 'Смена пароля Carrentino')

    async def change_password(self, data: ChangePasswordTokenReq) -> None:
        user = await self.user_repository.get_one_by(email=data.email)
        if user is None:
            raise UserNotFoundError
        async with RedisClient(get_settings().redis.url, db=get_settings().redis.email_code_db) as rc:
            saved_code = await rc.get(data.email)
        if saved_code is None or saved_code != data.code:
            raise InvalidCodeError
        user.password = await self.user_repository.hash_password(data.password)
        await self.user_repository.update_object(user)

    async def update_score(self, user_id: UUID, score: Decimal) -> None:
        user = await self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundError
        user.score = score
        await self.user_repository.update_object(user)

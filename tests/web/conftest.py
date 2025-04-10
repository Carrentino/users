from datetime import datetime, timedelta

import pytest
from helpers.enums.auth import TokenType
from helpers.models.user import UserContext, UserStatus
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user import User
from src.repositories.user import UserRepository
from src.web.depends.repository import get_user_repository
from tests.factories.user import UserFactory


@pytest.fixture()
async def user_repository(session: AsyncSession) -> UserRepository:
    return await get_user_repository(session)


@pytest.fixture()
async def user() -> User:
    return await UserFactory.create()


@pytest.fixture()
async def user_context(user: User) -> UserContext:
    return UserContext(
        user_id=str(user.id), status=UserStatus.VERIFIED, type=TokenType.ACCESS, exp=datetime.now() + timedelta(days=7)
    )

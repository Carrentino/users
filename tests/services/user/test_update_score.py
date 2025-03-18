from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.errors.service import UserNotFoundError
from src.services.user import UserService
from tests.factories.user import UserFactory


async def test_update_score_ok(user_service: UserService, session: AsyncSession) -> None:
    user = await UserFactory.create()
    await user_service.update_score(user.id, Decimal('4.0'))
    await session.refresh(user)
    assert user.score == Decimal('4.0')


async def test_update_score_nf(user_service: UserService) -> None:
    with pytest.raises(UserNotFoundError):
        await user_service.update_score(uuid4(), Decimal('4.0'))

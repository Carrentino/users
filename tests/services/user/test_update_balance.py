from decimal import Decimal
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from src.db.enums.user import UserStatus
from src.errors.service import UserNotFoundError, InvalidUserStatusError
from src.services.user import UserService
from tests.factories.user import UserFactory


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_update_balance(mock_redis: AsyncMock, user_service: UserService) -> None:
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.set.return_value = None
    user = await UserFactory.create(status=UserStatus.VERIFIED)
    balance = Decimal(100.10)
    await user_service.update_balance(user.id, balance)
    mock_redis_instance.set.assert_called_with(str(user.id), str(balance))


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_update_balance_nf_user(mock_redis: AsyncMock, user_service: UserService) -> None:
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.set.return_value = None
    balance = Decimal(100.10)
    with pytest.raises(UserNotFoundError):
        await user_service.update_balance(uuid4(), balance)
    mock_redis_instance.set.assert_not_called()


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_update_balance_na_user(mock_redis: AsyncMock, user_service: UserService) -> None:
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.set.return_value = None
    balance = Decimal(100.10)
    user = await UserFactory.create(status=UserStatus.BANNED)
    with pytest.raises(InvalidUserStatusError):
        await user_service.update_balance(user.id, balance)
    mock_redis_instance.set.assert_not_called()

from decimal import Decimal
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.db.enums.user import UserStatus
from src.kafka.payment.schemas import UpdateBalanceMessage, UpdateBalance
from src.services.user import UserService
from tests.factories.user import UserFactory


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_update_balance(mock_redis: AsyncMock, user_service: UserService) -> None:
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.set.return_value = None
    user = await UserFactory.create(status=UserStatus.VERIFIED)
    balance = Decimal(100.10)
    message = UpdateBalanceMessage(
        balances=[UpdateBalance(user_id=user.id, balance=balance)],
    )
    await user_service.update_balance(message)
    mock_redis_instance.set.assert_called_with(str(user.id), str(balance))


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_update_balance_nf_user(mock_redis: AsyncMock, user_service: UserService) -> None:
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.set.return_value = None
    balance = Decimal(100.10)
    message = UpdateBalanceMessage(
        balances=[UpdateBalance(user_id=uuid4(), balance=balance)],
    )
    await user_service.update_balance(message)
    mock_redis_instance.set.assert_not_called()


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_update_balance_na_user(mock_redis: AsyncMock, user_service: UserService) -> None:
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.set.return_value = None
    balance = Decimal(100.10)
    user = await UserFactory.create(status=UserStatus.BANNED)
    message = UpdateBalanceMessage(
        balances=[UpdateBalance(user_id=user.id, balance=balance)],
    )
    await user_service.update_balance(message)
    mock_redis_instance.set.assert_not_called()

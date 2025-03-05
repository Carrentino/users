import uuid
from unittest.mock import patch, AsyncMock

import pytest
from httpx import AsyncClient
from starlette import status

from src.db.enums.user import UserStatus
from tests.factories.user import UserFactory


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_verify_code_ok(mock_redis: AsyncMock, client: AsyncClient) -> None:
    user = await UserFactory.create(status=UserStatus.NOT_REGISTERED)
    req = {
        'user_id': str(user.id),
        'code': '000000',
    }
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = '000000'
    response = await client.post('/api/users/verify-code/', json=req)
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_verify_code_not_exists(mock_redis: AsyncMock, client: AsyncClient) -> None:
    req = {
        'user_id': str(uuid.uuid4()),
        'code': '000000',
    }
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    response = await client.post('/api/users/verify-code/', json=req)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_verify_code_invalid_status(mock_redis: AsyncMock, client: AsyncClient) -> None:
    user = await UserFactory.create(status=UserStatus.NOT_VERIFIED)
    req = {
        'user_id': str(user.id),
        'code': '000000',
    }
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    response = await client.post('/api/users/verify-code/', json=req)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize('code', [None, '000001'])
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_verify_code_invalid_code(mock_redis: AsyncMock, client: AsyncClient, code: str | None) -> None:
    user = await UserFactory.create(status=UserStatus.NOT_REGISTERED)
    req = {
        'user_id': str(user.id),
        'code': '000000',
    }
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = code
    response = await client.post('/api/users/verify-code/', json=req)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

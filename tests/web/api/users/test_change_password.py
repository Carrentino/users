from unittest.mock import patch, AsyncMock

import pytest
from httpx import AsyncClient
from starlette import status

from tests.factories.user import UserFactory


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_change_password_ok(mock_redis: AsyncMock, client: AsyncClient) -> None:
    user = await UserFactory.create()
    req = {
        'code': '000000',
        'email': user.email,
        'password': 'test_password',
    }
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = '000000'
    response = await client.post('/users/api/users/change-password/', json=req)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_change_password_nf(mock_redis: AsyncMock, client: AsyncClient) -> None:
    req = {
        'code': '000000',
        'email': 'test1@test.ru',
        'password': 'test_password',
    }
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = '000000'
    response = await client.post('/users/api/users/change-password/', json=req)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize('code', [None, '000001'])
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_change_password_invalid_code(mock_redis: AsyncMock, client: AsyncClient, code: str | None) -> None:
    user = await UserFactory.create()
    req = {
        'code': '000000',
        'email': user.email,
        'password': 'test_password',
    }
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = code
    response = await client.post('/users/api/users/change-password/', json=req)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

from unittest.mock import patch, AsyncMock

import pytest
from httpx import AsyncClient
from starlette import status


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_verify_code_ok(mock_redis: AsyncMock, client: AsyncClient) -> None:
    req = {
        'code': '000000',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test1@test.ru',
        'phone_number': '+79999999991',
        'password': 'test_password',
    }
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = '000000'
    response = await client.post('/api/users/verify-code/', json=req)
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()


@pytest.mark.parametrize('code', [None, '000001'])
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_verify_code_invalid_code(mock_redis: AsyncMock, client: AsyncClient, code: str | None) -> None:
    req = {
        'code': '000000',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test1@test.ru',
        'phone_number': '+79999999991',
        'password': 'test_password',
    }
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = code
    response = await client.post('/api/users/verify-code/', json=req)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

from unittest.mock import patch, AsyncMock

from httpx import AsyncClient
from starlette import status

from tests.factories.user import UserFactory


@patch('src.integrations.notifications.NotificationsClient.send_email_code', new_callable=AsyncMock)
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_registration(mock_redis: AsyncMock, mock_send: AsyncMock, client: AsyncClient) -> None:
    req = {
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@test.ru',
        'phone_number': '+79999999999',
        'password': 'test_password',
    }
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    response = await client.post('/api/users/registration/', json=req)
    assert response.status_code == status.HTTP_200_OK


@patch('src.integrations.notifications.NotificationsClient.send_email_code', new_callable=AsyncMock)
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_registration_exists(mock_redis: AsyncMock, mock_send: AsyncMock, client: AsyncClient) -> None:
    await UserFactory.create(first_name='test', last_name='test', email='test1@test.ru', phone_number='+79999999991')
    req = {
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test1@test.ru',
        'phone_number': '+79999999991',
        'password': 'test_password',
    }
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    response = await client.post('/api/users/registration/', json=req)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

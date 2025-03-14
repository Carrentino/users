from unittest.mock import patch, AsyncMock

from httpx import AsyncClient
from starlette import status

from tests.factories.user import UserFactory


@patch('src.integrations.notifications.NotificationsClient.send_email_notification', new_callable=AsyncMock)
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_change_password_code_ok(mock_redis: AsyncMock, mock_send: AsyncMock, client: AsyncClient) -> None:
    user = await UserFactory.create()
    req = {
        'email': user.email,
    }
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    response = await client.post('/api/users/change-password/send-code/', json=req)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@patch('src.integrations.notifications.NotificationsClient.send_email_notification', new_callable=AsyncMock)
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_change_password_code_nf(mock_redis: AsyncMock, mock_send: AsyncMock, client: AsyncClient) -> None:
    req = {
        'email': 'test@test.ru',
    }
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    response = await client.post('/api/users/change-password/send-code/', json=req)
    assert response.status_code == status.HTTP_404_NOT_FOUND

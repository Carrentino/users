from unittest.mock import patch, AsyncMock

from httpx import AsyncClient
from starlette import status


@patch('src.integrations.notifications.NotificationsClient.send_email_notification', new_callable=AsyncMock)
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_registration(mock_redis: AsyncMock, mock_send: AsyncMock, client: AsyncClient) -> None:
    req = {
        'email': 'test@test.ru',
    }
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    response = await client.post('/users/api/users/registration/', json=req)
    assert response.status_code == status.HTTP_200_OK

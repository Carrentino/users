from unittest.mock import patch, AsyncMock

from httpx import AsyncClient
from starlette import status

from src.web.api.me.schemas import UserProfile


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
@patch('src.integrations.payment.PaymentClient.get_user_balance', new_callable=AsyncMock)
async def test_profile(mock_get: AsyncMock, mock_redis: AsyncMock, auth_client: AsyncClient) -> None:
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = 123
    response = await auth_client.get('/api/me/')
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()
    mock_get.assert_not_called()
    assert json_resp == UserProfile.model_validate(json_resp).model_dump(mode='json')
    assert json_resp['balance'] == 123


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
@patch('src.integrations.payment.PaymentClient.get_user_balance', new_callable=AsyncMock)
async def test_profile_with_payments(mock_get: AsyncMock, mock_redis: AsyncMock, auth_client: AsyncClient) -> None:
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = None
    mock_get.return_value = 123

    response = await auth_client.get('/api/me/')
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()
    mock_get.assert_called_once()
    assert json_resp == UserProfile.model_validate(json_resp).model_dump(mode='json')
    assert json_resp['balance'] == 123

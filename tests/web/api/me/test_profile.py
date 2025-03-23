from unittest.mock import patch, AsyncMock
from uuid import uuid4

from helpers.models.user import UserContext
from httpx import AsyncClient
from starlette import status

from src.web.api.me.schemas import UserProfile
from tests.factories.user import UserFactory


@patch('src.integrations.reviews.ReviewsClient.get_reviews', new_callable=AsyncMock)
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
@patch('src.integrations.payment.PaymentClient.get_user_balance', new_callable=AsyncMock)
async def test_profile(
    mock_get: AsyncMock,
    mock_redis: AsyncMock,
    mock_get_reviews: AsyncMock,
    user_context: UserContext,
    auth_client: AsyncClient,
) -> None:
    mock_redis_instance = AsyncMock()

    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = 123
    mock_get_reviews.return_value = []
    response = await auth_client.get(f'/users/api/me/{user_context.user_id}/')
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()
    mock_get.assert_not_called()
    assert json_resp == UserProfile.model_validate(json_resp).model_dump(mode='json')
    assert json_resp['balance'] == 123


@patch('src.integrations.reviews.ReviewsClient.get_reviews', new_callable=AsyncMock)
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
@patch('src.integrations.payment.PaymentClient.get_user_balance', new_callable=AsyncMock)
async def test_profile_with_payments(
    mock_get: AsyncMock,
    mock_redis: AsyncMock,
    mock_get_reviews: AsyncMock,
    user_context: UserContext,
    auth_client: AsyncClient,
) -> None:
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = None
    mock_get.return_value = 123
    mock_get_reviews.return_value = []

    response = await auth_client.get(f'/users/api/me/{user_context.user_id}/')
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()
    mock_get.assert_called_once()
    assert json_resp == UserProfile.model_validate(json_resp).model_dump(mode='json')
    assert json_resp['balance'] == 123


@patch('src.integrations.reviews.ReviewsClient.get_reviews', new_callable=AsyncMock)
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
@patch('src.integrations.payment.PaymentClient.get_user_balance', new_callable=AsyncMock)
async def test_profile_nf(
    mock_get: AsyncMock, mock_redis: AsyncMock, mock_get_reviews: AsyncMock, auth_client: AsyncClient
) -> None:
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = None
    mock_get.return_value = 123
    mock_get_reviews.return_value = []

    response = await auth_client.get(f'/users/api/me/{uuid4()}/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch('src.integrations.reviews.ReviewsClient.get_reviews', new_callable=AsyncMock)
@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
@patch('src.integrations.payment.PaymentClient.get_user_balance', new_callable=AsyncMock)
async def test_profile_another_user(
    mock_get: AsyncMock, mock_redis: AsyncMock, mock_get_reviews: AsyncMock, auth_client: AsyncClient
) -> None:
    user = await UserFactory.create()
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.get.return_value = None
    mock_get.return_value = 123
    mock_get_reviews.return_value = []

    response = await auth_client.get(f'/users/api/me/{user.id}/')
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()
    assert json_resp['balance'] is None
    assert json_resp['email'] is None

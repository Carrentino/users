from unittest.mock import patch, AsyncMock
from uuid import UUID

from helpers.models.user import UserContext
from httpx import AsyncClient
from starlette import status

from tests.factories.user_favorite import UserFavoriteFactory


@patch('src.integrations.cars.CarsClient.get_cars', new_callable=AsyncMock)
@patch('src.repositories.user_favorite.UserFavoriteRepository.get_list', return_value=[])
async def test_get_favorites(
    mock_get_list: AsyncMock, mock_get_cars: AsyncMock, user_context: UserContext, auth_client: AsyncClient
):

    favorites = [
        await UserFavoriteFactory.create(),
        await UserFavoriteFactory.create(),
        await UserFavoriteFactory.create(),
        await UserFavoriteFactory.create(),
    ]
    mock_get_list.return_value = favorites
    response = await auth_client.get("/api/me/favorites/")
    mock_get_list.assert_called_once_with(user_id=UUID(user_context.user_id))
    mock_get_cars.assert_called_once_with([item.car_id for item in favorites], 30, 0)
    assert response.status_code == status.HTTP_200_OK

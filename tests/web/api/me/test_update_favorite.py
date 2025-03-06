import uuid

from httpx import AsyncClient
from starlette import status


async def test_update_favorite(auth_client: AsyncClient) -> None:
    req = {"car_id": str(uuid.uuid4())}
    response = await auth_client.put('/api/me/favorite/', json=req)
    assert response.status_code == status.HTTP_200_OK

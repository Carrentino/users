from starlette import status

from tests.factories.user import UserFactory


async def test_get_users_by_ids(client) -> None:
    users = [
        await UserFactory.create(),
        await UserFactory.create(),
        await UserFactory.create(),
        await UserFactory.create(),
    ]
    url = f"/api/users/?user__id={users[0].id}"
    for i in range(1, len(users)):
        url = f"{url}&user__id={users[i].id}"
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()
    assert len(json_resp) == len(users)

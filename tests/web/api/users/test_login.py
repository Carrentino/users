import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.enums.user import UserStatus
from src.repositories.user import UserRepository
from tests.factories.user import UserFactory


@pytest.mark.parametrize(
    ('req', 'status'),
    [
        (
            {
                'email': 'verify@test.ru',
                'password': 'password',
            },
            status.HTTP_200_OK,
        ),
        (
            {
                'email': 'verify@test.ru',
                'password': 'pass',
            },
            status.HTTP_403_FORBIDDEN,
        ),
        (
            {
                'email': 'test@test.ru',
                'password': 'password',
            },
            status.HTTP_404_NOT_FOUND,
        ),
    ],
)
async def test_login(
    session: AsyncSession, client: AsyncClient, user_repository: UserRepository, req: dict[str, str], status: int
) -> None:
    hashed_password = user_repository.hash_password('password')
    user = await UserFactory.create(email='verify@test.ru', password=hashed_password, status=UserStatus.VERIFIED)
    response = await client.post('/api/users/login/', json=req)
    assert response.status_code == status
    await session.delete(user)
    await session.commit()


async def test_login_invalid_status(
    session: AsyncSession, client: AsyncClient, user_repository: UserRepository
) -> None:
    hashed_password = user_repository.hash_password('password')
    user = await UserFactory.create(email='verify@test.ru', password=hashed_password, status=UserStatus.BANNED)
    req = {
        'email': 'verify@test.ru',
        'password': 'password',
    }
    response = await client.post('/api/users/login/', json=req)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    await session.delete(user)
    await session.commit()

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user import UserRepository
from src.web.depends.repository import get_user_repository


@pytest.fixture()
async def user_repository(session: AsyncSession) -> UserRepository:
    return await get_user_repository(session)

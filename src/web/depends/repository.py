from typing import Annotated

from fastapi import Depends
from helpers.depends.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user import UserRepository
from src.repositories.user_favorite import UserFavoriteRepository


async def get_user_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserRepository:
    return UserRepository(session=session)


async def get_user_favorite_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserFavoriteRepository:
    return UserFavoriteRepository(session=session)

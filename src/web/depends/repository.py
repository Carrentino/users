from typing import Annotated

from fastapi import Depends
from helpers.depends.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_repository import UserRepository


async def get_user_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserRepository:
    return UserRepository(session=session)

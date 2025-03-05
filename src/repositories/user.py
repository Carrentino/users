import asyncio

import bcrypt
from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.user import User


class UserRepository(ISqlAlchemyRepository[User]):
    _model = User

    @staticmethod
    async def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return await asyncio.to_thread(lambda: bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8'))

    @staticmethod
    async def verify_password(password: str, hashed_password: str) -> bool:
        return await asyncio.to_thread(
            lambda: bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        )

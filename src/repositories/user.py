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

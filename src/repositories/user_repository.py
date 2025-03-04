import asyncio

import bcrypt
from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository


class UserRepository[User](ISqlAlchemyRepository):
    _model = User

    async def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return await asyncio.to_thread(lambda: bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8'))

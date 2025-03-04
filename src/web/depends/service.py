from typing import Annotated

from fastapi import Depends

from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from src.web.depends.repository import get_user_repository


async def get_user_service(user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> UserService:
    return UserService(user_repository=user_repository)

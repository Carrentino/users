from typing import Annotated

from fastapi import Depends

from src.integrations.notifications import NotificationsClient
from src.repositories.user import UserRepository
from src.repositories.user_favorite import UserFavoriteRepository
from src.services.user import UserService
from src.services.user_favorite import UserFavoriteService
from src.web.depends.integrations import get_notifications_client
from src.web.depends.repository import get_user_repository, get_user_favorite_repository


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    notifications_client: Annotated[NotificationsClient, Depends(get_notifications_client)],
) -> UserService:
    return UserService(user_repository=user_repository, notifications_client=notifications_client)


async def get_user_favorite_service(
    user_favorite_repository: Annotated[UserFavoriteRepository, Depends(get_user_favorite_repository)],
) -> UserFavoriteService:
    return UserFavoriteService(
        user_favorite_repository=user_favorite_repository,
    )

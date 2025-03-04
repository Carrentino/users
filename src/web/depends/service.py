from typing import Annotated

from fastapi import Depends

from src.integrations.notifications import NotificationsClient
from src.repositories.user_repository import UserRepository
from src.services.user import UserService
from src.web.depends.integrations import get_notifications_client
from src.web.depends.repository import get_user_repository


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    notifications_client: Annotated[NotificationsClient, Depends(get_notifications_client)],
) -> UserService:
    return UserService(user_repository=user_repository, notifications_client=notifications_client)

from typing import Annotated

from fastapi import Depends

from src.integrations.cars import CarsClient
from src.integrations.notifications import NotificationsClient
from src.integrations.payment import PaymentClient
from src.integrations.reviews import ReviewsClient
from src.repositories.user import UserRepository
from src.repositories.user_favorite import UserFavoriteRepository
from src.services.user import UserService
from src.services.user_favorite import UserFavoriteService
from src.web.depends.integrations import (
    get_notifications_client,
    get_payment_client,
    get_cars_client,
    get_reviews_client,
)
from src.web.depends.repository import get_user_repository, get_user_favorite_repository


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    notifications_client: Annotated[NotificationsClient, Depends(get_notifications_client)],
    payment_client: Annotated[PaymentClient, Depends(get_payment_client)],
    reviews_client: Annotated[ReviewsClient, Depends(get_reviews_client)],
) -> UserService:
    return UserService(
        user_repository=user_repository,
        notifications_client=notifications_client,
        payment_client=payment_client,
        reviews_client=reviews_client,
    )


async def get_user_favorite_service(
    user_favorite_repository: Annotated[UserFavoriteRepository, Depends(get_user_favorite_repository)],
    cars_client: Annotated[CarsClient, Depends(get_cars_client)],
) -> UserFavoriteService:
    return UserFavoriteService(
        user_favorite_repository=user_favorite_repository,
        cars_client=cars_client,
    )

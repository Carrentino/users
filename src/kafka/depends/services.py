from sqlalchemy.ext.asyncio import AsyncSession

from src.services.user import UserService
from src.web.depends.integrations import get_notifications_client, get_payment_client, get_reviews_client
from src.web.depends.repository import get_user_repository


async def get_user_service(session: AsyncSession) -> UserService:
    return UserService(
        user_repository=await get_user_repository(session=session),
        notifications_client=await get_notifications_client(),
        payment_client=await get_payment_client(),
        reviews_client=await get_reviews_client(),
    )

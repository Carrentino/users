from src.integrations.notifications import NotificationsClient
from src.integrations.payment import PaymentClient


async def get_notifications_client() -> NotificationsClient:
    return NotificationsClient()


async def get_payment_client() -> PaymentClient:
    return PaymentClient()

from src.integrations.notifications import NotificationsClient


async def get_notifications_client() -> NotificationsClient:
    return NotificationsClient()

from src.bootstrap import get_kafka_producer
from src.integrations.cars import CarsClient
from src.integrations.notifications import NotificationsClient
from src.integrations.payment import PaymentClient
from src.integrations.reviews import ReviewsClient


async def get_notifications_client() -> NotificationsClient:
    return get_kafka_producer()


async def get_payment_client() -> PaymentClient:
    return PaymentClient()


async def get_cars_client() -> CarsClient:
    return CarsClient()


async def get_reviews_client() -> ReviewsClient:
    return ReviewsClient()

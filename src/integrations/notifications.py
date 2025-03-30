from helpers.kafka.producer import KafkaProducer

from src.integrations.schemas.notifications import EmailNotification
from src.settings import get_settings


class NotificationsClient(KafkaProducer):
    email_topic = get_settings().kafka.topic_email_notifications

    def __init__(self) -> None:
        super().__init__(str(get_settings().kafka.bootstrap_servers))

    async def send_email_notification(self, message: EmailNotification) -> None:
        await self.send_model_message(self.email_topic, message)

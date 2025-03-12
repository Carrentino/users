from helpers.depends.db_session import get_db_session_context
from helpers.kafka.consumer import KafkaConsumerTopicsListeners

from src.kafka.db_client import make_db_client
from src.kafka.payment.schemas import UpdateBalance
from src.web.depends.integrations import get_notifications_client, get_payment_client, get_reviews_client
from src.web.depends.repository import get_user_repository
from src.web.depends.service import get_user_service

payment_listener = KafkaConsumerTopicsListeners()


@payment_listener.add("user_balance", UpdateBalance)
async def update_balance(
    message: UpdateBalance,
) -> None:
    async with get_db_session_context(make_db_client()) as session:
        user_service = await get_user_service(
            user_repository=await get_user_repository(session=session),
            notifications_client=await get_notifications_client(),
            payment_client=await get_payment_client(),
            reviews_client=await get_reviews_client(),
        )
    await user_service.update_balance(message.user_id, message.balance)

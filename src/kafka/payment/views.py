from helpers.depends.db_session import get_db_session_context
from helpers.kafka.consumer import KafkaConsumerTopicsListeners

from src.kafka.db_client import make_db_client
from src.kafka.depends import get_user_service
from src.kafka.payment.schemas import UpdateBalance
from src.settings import get_settings

payment_listener = KafkaConsumerTopicsListeners()


@payment_listener.add(get_settings().kafka.topic_user_balance, UpdateBalance)
async def update_balance(
    message: UpdateBalance,
) -> None:
    async with get_db_session_context(make_db_client()) as session:
        user_service = await get_user_service(session)
        await user_service.update_balance(message.user_id, message.balance)

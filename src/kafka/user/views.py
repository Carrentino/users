from helpers.depends.db_session import get_db_session_context
from helpers.kafka.consumer import KafkaConsumerTopicsListeners

from src.kafka.db_client import make_db_client
from src.kafka.depends.services import get_user_service
from src.kafka.user.schemas import UpdateScore
from src.settings import get_settings

user_listener = KafkaConsumerTopicsListeners()


@user_listener.add(get_settings().kafka.topic_user_score, UpdateScore)
async def update_score(
    message: UpdateScore,
) -> None:
    async with get_db_session_context(make_db_client()) as session:
        user_service = await get_user_service(session)
        await user_service.update_score(message.user_id, message.score)

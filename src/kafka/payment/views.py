from typing import Annotated

from fastapi import Depends
from helpers.kafka.consumer import KafkaConsumerTopicsListeners

from src.kafka.payment.schemas import UpdateBalance
from src.services.user import UserService
from src.web.depends.service import get_user_service

payment_listener = KafkaConsumerTopicsListeners()


@payment_listener.add("user_balance", UpdateBalance)
async def update_balance(
    user_service: Annotated[UserService, Depends(get_user_service)],
    message: UpdateBalance,
) -> None:
    await user_service.update_balance(message.user_id, message.balance)

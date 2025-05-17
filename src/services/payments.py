from src.integrations.payment import PaymentClient
from src.web.api.payments.schemas import DepositOrWithdrawReq, TransactionFilters


class PaymentsService:
    def __init__(self, payments_client: PaymentClient):
        self.payments_client = payments_client

    async def process_payment(self, data: DepositOrWithdrawReq, user_id: str):
        return await self.payments_client.process_payment(data, user_id)

    async def get_transactions(self, user_id: str, filters: TransactionFilters):
        return await self.payments_client.get_transactions(user_id, filters)

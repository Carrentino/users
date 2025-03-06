from uuid import UUID

from helpers.clients.http_client import BaseApiClient


class PaymentClient(BaseApiClient):
    _base_url = ''

    async def get_user_balance(self, _: UUID) -> int:

        # TODO: сделать когда будет готов сервис платежей
        return 0

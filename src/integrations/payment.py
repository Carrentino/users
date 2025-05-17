from uuid import UUID

from helpers.clients.http_client import BaseApiClient

from src.errors.http import PaymentServiceIsOffHttpError
from src.web.api.payments.schemas import DepositOrWithdrawReq, TransactionFilters


class PaymentClient(BaseApiClient):
    _base_url = ''

    async def get_user_balance(self, _: UUID) -> int:

        # TODO: сделать когда будет готов сервис платежей
        return 0

    async def process_payment(self, data: DepositOrWithdrawReq, user_id: str):
        req_data = data.model_dump(mode="python")
        req_data["user_id"] = UUID(user_id)
        resp = await self.post(self._base_url.join('transactions/'))
        try:
            resp.raise_for_status()
        except:  # noqa: E722
            raise PaymentServiceIsOffHttpError from None
        return resp.json()

    async def get_transactions(self, user_id: str, filters: TransactionFilters):
        req_filters = filters.model_dump(mode='python', exclude_none=True)
        resp = await self.get(self._base_url.join(f'transactions/{user_id}/'), params=req_filters)
        try:
            resp.raise_for_status()
        except:  # noqa: E722
            raise PaymentServiceIsOffHttpError from None
        return resp.json()

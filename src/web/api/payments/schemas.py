from decimal import Decimal

from pydantic import BaseModel


class DepositOrWithdrawReq(BaseModel):
    amount: Decimal
    transaction_type: str
    payment_redirect: str | None = None
    description: str | None = None
    card_number: str | None = None


class DepositOrWithdrawResp(BaseModel):
    confirmation_url: str | None = None


class TransactionFilters(BaseModel):
    transaction_type: str | None = None
    status: str | None = None

    offset: int = 0
    limit: int = 30

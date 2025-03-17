from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class UpdateBalance(BaseModel):
    user_id: UUID
    balance: Decimal


class UpdateBalanceMessage(BaseModel):
    balances: list[UpdateBalance]

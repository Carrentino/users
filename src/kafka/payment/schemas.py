from uuid import UUID

from pydantic import BaseModel


class UpdateBalance(BaseModel):
    user_id: UUID
    balance: int

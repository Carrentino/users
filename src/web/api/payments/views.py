from typing import Annotated

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext

from src.services.payments import PaymentsService
from src.web.api.payments.schemas import DepositOrWithdrawReq, DepositOrWithdrawResp, TransactionFilters
from src.web.depends.service import get_payments_service

payments_router = APIRouter()


@payments_router.post('/process-payment')
async def process_payment(
    payments_service: Annotated[PaymentsService, Depends(get_payments_service)],
    user: Annotated[UserContext, Depends(get_current_user)],
    data: DepositOrWithdrawReq,
) -> DepositOrWithdrawResp:
    return await payments_service.process_payment(data, user.user_id)


@payments_router.get('/')
async def get_transactions(
    payments_service: Annotated[PaymentsService, Depends(get_payments_service)],
    user: Annotated[UserContext, Depends(get_current_user)],
    filters: TransactionFilters = Depends(),
):
    return await payments_service.get_transactions(user.user_id, filters)

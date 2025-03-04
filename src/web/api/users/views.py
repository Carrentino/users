from typing import Annotated

from fastapi import APIRouter, Depends

from src.errors.http import UserAlreadyExistsErrorHttpError
from src.errors.service import UserAlreadyExistsError
from src.services.user_service import UserService
from src.web.api.users.schemas import UserRegistrationReq
from src.web.depends.service import get_user_service

users_router = APIRouter()


@users_router.post('registration/')
async def registration(
    user_service: Annotated[UserService, Depends(get_user_service)],
    req_data: UserRegistrationReq,
):
    try:
        await user_service.registration(req_data)
    except UserAlreadyExistsError:
        raise UserAlreadyExistsErrorHttpError from None

from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.errors.http import (
    UserAlreadyExistsErrorHttpError,
    UserNotFoundHttpError,
    InvalidUserStatusHttpError,
    InvalidCodeHttpError,
    WrongPasswordHttpError,
)
from src.errors.service import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidUserStatusError,
    InvalidCodeError,
    WrongPasswordError,
)
from src.services.user import UserService
from src.web.api.users.schemas import (
    UserRegistrationReq,
    TokenResponse,
    VerifyTokenReq,
    UserLoginReq,
    UsersFilterId,
    ChangePasswordSendCodeReq,
    ChangePasswordTokenReq,
)
from src.web.depends.service import get_user_service

users_router = APIRouter()


@users_router.post('/registration/')
async def registration(
    user_service: Annotated[UserService, Depends(get_user_service)],
    req_data: UserRegistrationReq,
):
    await user_service.registration(req_data)


@users_router.post('/verify-code/')
async def verify_code(
    user_service: Annotated[UserService, Depends(get_user_service)],
    req_data: VerifyTokenReq,
) -> TokenResponse:
    try:
        return await user_service.verify_code(user=req_data)
    except InvalidCodeError:
        raise InvalidCodeHttpError from None
    except UserAlreadyExistsError:
        raise UserAlreadyExistsErrorHttpError from None


@users_router.post('/login/')
async def login(
    user_service: Annotated[UserService, Depends(get_user_service)],
    req_data: UserLoginReq,
) -> TokenResponse:
    try:
        return await user_service.login(email=req_data.email, password=req_data.password)
    except UserNotFoundError:
        raise UserNotFoundHttpError from None
    except WrongPasswordError:
        raise WrongPasswordHttpError from None
    except InvalidUserStatusError:
        raise InvalidUserStatusHttpError from None


@users_router.get('/')
async def get_users_by_ids(
    user_service: Annotated[UserService, Depends(get_user_service)],
    filters: UsersFilterId = Depends(),
):
    return await user_service.get_users_by_ids(filters)


@users_router.post('/change-password/send-code/', status_code=status.HTTP_204_NO_CONTENT)
async def change_password_send_code(
    user_service: Annotated[UserService, Depends(get_user_service)],
    req: ChangePasswordSendCodeReq,
) -> None:
    try:
        await user_service.send_code_to_change_password(req.email)
    except UserNotFoundError:
        raise UserNotFoundHttpError from None


@users_router.post('/change-password/', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user_service: Annotated[UserService, Depends(get_user_service)],
    req: ChangePasswordTokenReq,
) -> None:
    try:
        await user_service.change_password(req)
    except UserNotFoundError:
        raise UserNotFoundHttpError from None
    except InvalidCodeError:
        raise InvalidCodeHttpError from None

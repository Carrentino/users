from typing import Annotated

from fastapi import APIRouter, Depends

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
from src.web.api.users.schemas import UserRegistrationReq, TokenResponse, VerifyTokenReq, UserLoginReq, UsersFilterId
from src.web.depends.service import get_user_service

users_router = APIRouter()


@users_router.post('/registration/')
async def registration(
    user_service: Annotated[UserService, Depends(get_user_service)],
    req_data: UserRegistrationReq,
):
    try:
        await user_service.registration(req_data)
    except UserAlreadyExistsError:
        raise UserAlreadyExistsErrorHttpError from None


@users_router.post('/verify-code/')
async def verify_code(
    user_service: Annotated[UserService, Depends(get_user_service)],
    req_data: VerifyTokenReq,
) -> TokenResponse:
    try:
        return await user_service.verify_code(user_id=req_data.user_id, code=req_data.code)
    except UserNotFoundError:
        raise UserNotFoundHttpError from None
    except InvalidUserStatusError:
        raise InvalidUserStatusHttpError from None
    except InvalidCodeError:
        raise InvalidCodeHttpError from None


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

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext
from starlette.requests import Request

from src.errors.http import UserNotFoundHttpError
from src.errors.service import UserNotFoundError
from src.integrations.schemas.cars import CarPaginatedResponse
from src.services.user import UserService
from src.services.user_favorite import UserFavoriteService
from src.web.api.me.schemas import UpdateFavoritesReq, UserProfile, FavoritesFilters
from src.web.depends.service import get_user_favorite_service, get_user_service

me_router = APIRouter()


@me_router.get('/favorites/')
async def get_favorites(
    user_favorite_service: Annotated[UserFavoriteService, Depends(get_user_favorite_service)],
    user_context: Annotated[UserContext, Depends(get_current_user)],
    filters: Annotated[FavoritesFilters, Depends()],
) -> CarPaginatedResponse:
    return await user_favorite_service.get_favorites(UUID(user_context.user_id), filters)


@me_router.post('/favorite/')
async def update_favorite(
    user_favorite_service: Annotated[UserFavoriteService, Depends(get_user_favorite_service)],
    user_context: Annotated[UserContext, Depends(get_current_user)],
    req_data: UpdateFavoritesReq,
) -> str:
    await user_favorite_service.update_favorite(user_context, req_data.car_id)
    return "OK"


@me_router.get('/{user_id}/')
async def profile(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_context: Annotated[UserContext, Depends(get_current_user)],
    user_id: UUID,
) -> UserProfile:
    try:
        return await user_service.get_user(user_id, UUID(user_context.user_id), request.headers.get('x-auth-token'))
    except UserNotFoundError:
        raise UserNotFoundHttpError from None

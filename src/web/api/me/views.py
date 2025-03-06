from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext

from src.services.user import UserService
from src.services.user_favorite import UserFavoriteService
from src.web.api.me.schemas import UpdateFavoritesReq, UserProfile
from src.web.depends.service import get_user_favorite_service

me_router = APIRouter()


@me_router.post('/favorite/')
async def update_favorite(
    user_favorite_service: Annotated[UserFavoriteService, Depends(get_user_favorite_service)],
    user_context: Annotated[UserContext, Depends(get_current_user)],
    req_data: UpdateFavoritesReq,
) -> str:
    await user_favorite_service.update_favorite(user_context, req_data.car_id)
    return "OK"


@me_router.get('/')
async def profile(
    user_service: Annotated[UserService, Depends(get_current_user)],
    user_context: Annotated[UserContext, Depends(get_current_user)],
) -> UserProfile:
    return await user_service.get_user(UUID(user_context.user_id))

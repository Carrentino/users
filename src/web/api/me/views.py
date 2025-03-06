from typing import Annotated

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext

from src.services.user_favorite import UserFavoriteService
from src.web.api.me.schemas import UpdateFavoritesReq
from src.web.depends.service import get_user_favorite_service

me_router = APIRouter()


@me_router.put('/favorite/')
async def update_favorite(
    user_favorite_service: Annotated[UserFavoriteService, Depends(get_user_favorite_service)],
    user_context: Annotated[UserContext, Depends(get_current_user)],
    req_data: UpdateFavoritesReq,
) -> str:
    await user_favorite_service.update_favorite(user_context, req_data.car_id)
    return "OK"

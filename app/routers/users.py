from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from app.models import UserModel
from app.security.jwt_token import get_current_active_user
from app.schemas.user import UserIn, UserOut
from app.services.user import UserService

router = APIRouter(
    tags=["users"]
)
user_service = UserService()



@router.get("/users/", status_code=200)
async def get_users() -> list[UserOut]:
    users = await user_service.get_users()
    return users


@router.get("/users/me/", response_model=UserOut)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return current_user



@router.put("/users/{user_id}/", status_code=200)
async def update_user(user_id: int, user_in: UserIn) -> UserOut:
    user = await user_service.update_user(user_id=user_id, username=user_in.username, password=user_in.password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

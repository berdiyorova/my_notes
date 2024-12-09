from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models import BlockedToken
from app.security.auth import get_password_hash, validate_password, check_user, validate_email_address, \
    verify_password, authenticate_user
from app.security.jwt_token import create_access_token
from app.schemas.user import UserIn, UserOut, Login, TokenData, Logout, StandardResponse

from app.services.user import UserService

router = APIRouter(
    tags=["Authentication"]
)
user_service = UserService()


@router.post('/register/', status_code=status.HTTP_201_CREATED)
async def register(user_in: UserIn) -> UserOut:
    await validate_email_address(email=user_in.email)
    await validate_password(password=user_in.password, confirm_password=user_in.confirm_password)
    await check_user(username=user_in.username, email=user_in.email)

    user_dict = user_in.dict()
    user_dict.pop("confirm_password")
    user_dict["password"] = await get_password_hash(user_in.password)

    user = await user_service.create_user(**user_dict)
    return user


@router.post('/login/')
async def login(data: Login) -> TokenData:
    user = await user_service.get_user_by_username(username=data.username)
    if not user or not await verify_password(plain_password=data.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is incorrect"
        )
    access_token = await create_access_token(data={"sub": user.username})
    return TokenData(access_token=access_token, token_type="bearer")


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenData:
    user = await authenticate_user(
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(data={"sub": user.username})
    return TokenData(access_token=access_token, token_type="bearer")


@router.post('/logout/')
async def logout(token: Logout) -> StandardResponse:
    blocked_token = BlockedToken(token=token.access_token)
    db = next(get_db())
    db.add(blocked_token)
    db.commit()
    db.refresh(blocked_token)
    return StandardResponse(success=True, message="Successfully logged out")

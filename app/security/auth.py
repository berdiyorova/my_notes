import re

from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.services.user import UserService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_service = UserService()


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



async def get_password_hash(password):
    return pwd_context.hash(password)



async def validate_password(password: str, confirm_password: str) -> None:
    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    elif len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password length must not be less than 8 characters"
        )
    elif (not re.search("[a-z]", password) or
          not re.search("[A-Z]", password) or
          not re.search("[0-9]", password)):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must include at least one lowercase letter, one uppercase letter, and one digit."
        )



async def validate_email_address(email: str) -> None | str:
    try:
        v = validate_email(email)
        # replace with normalized form
        email = v["email"]
        return email

    except EmailNotValidError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )



async def check_user(username: str, email: str) -> None:
    if await user_service.get_user_by_username(username=username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )



async def authenticate_user(username: str, password: str):
    user = await user_service.get_user_by_username(username)
    if not user:
        return False
    if not await verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user

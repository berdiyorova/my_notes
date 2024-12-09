from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=100)


class UserIn(UserBase):
    password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)


class UserOut(UserBase):
    id: int


class Login(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    username: str


class Logout(BaseModel):
    access_token: str


class StandardResponse(BaseModel):
    success: bool
    message: str

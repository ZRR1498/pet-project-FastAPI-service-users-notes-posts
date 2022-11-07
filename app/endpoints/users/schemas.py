import datetime

from pydantic import BaseModel


class UserLoginForm(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    nickname: str
    is_active: bool

    class Config:
        orm_mode = True


class UserCreateForm(UserBase):
    password: str


class UserProfile(UserBase):
    id: int


class UsersAll(BaseModel):
    id: int
    nickname: str

    class Config:
        orm_mode = True


class UserUpdateData(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    is_active: bool


class UserGetByNickname(UsersAll):
    nickname: str
    first_name: str
    last_name: str
    avatar: str | None
    is_active: bool
    created_at: datetime.date


class UserId(BaseModel):
    id: int

import datetime

from pydantic import BaseModel, Field, EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        orm_mode = True


class UsersGet(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    nickname: str
    is_active: bool
    avatar: str | None
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class UserId(BaseModel):
    id: int

    class Config:
        orm_mode = True

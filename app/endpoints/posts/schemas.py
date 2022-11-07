import datetime

from pydantic import BaseModel


class PostUserGet(BaseModel):
    id: int
    text: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    likes: int | None

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    text: str

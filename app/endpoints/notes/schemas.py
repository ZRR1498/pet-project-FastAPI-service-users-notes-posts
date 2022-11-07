import datetime

from pydantic import BaseModel


class NotesCreate(BaseModel):
    title: str | None
    description: str | None


class NotesGet(BaseModel):
    id: int
    title: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None

    class Config:
        orm_mode = True


class NoteCurrentGet(NotesGet):
    description: str


class NoteUpdate(NotesCreate):

    class Config:
        orm_mode = True

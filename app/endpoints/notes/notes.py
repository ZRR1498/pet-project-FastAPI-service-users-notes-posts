import datetime

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.endpoints.notes.models import Notes
from app.endpoints.notes.schemas import NotesCreate, NotesGet, NoteUpdate, NoteCurrentGet
from app.endpoints.users.models import AuthToken
from app.utils import check_auth_token

router = APIRouter()


@router.post("/user/notes/", name="create_note", tags=["notes"])
async def create_note(token: AuthToken = Depends(check_auth_token), note: NotesCreate = Body(..., embed=True),
                      db: Session = Depends(get_db)):
    if token:
        if note.title != "" and note.description != "":
            note_data = Notes(
                user_id=token.user_id,
                title=note.title,
                description=note.description
            )
            db.add(note_data)
            db.commit()

            return {"notes_id": note_data.id}

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please fill all fields")


@router.get("/user/notes/", response_model=List[NotesGet], name="get_all_notes", tags=["notes"])
async def get_all_notes(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    if token:
        notes = db.query(Notes).filter(Notes.user_id == token.user_id, Notes.status_delete == False). \
            order_by(Notes.id.desc()).all()
        if not notes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found notes")

        return notes


@router.get("/user/notes/deleted", response_model=List[NotesGet], name="get_deleted_notes", tags=["notes"])
async def get_all_notes(token: AuthToken = Depends(check_auth_token), db: Session = Depends(get_db)):
    if token:
        notes = db.query(Notes).filter(Notes.user_id == token.user_id, Notes.status_delete == True). \
            order_by(Notes.created_at.desc()).all()
        if not notes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found deleted notes")

        return notes


@router.get("/user/notes/deleted/{note_id}/", response_model=NoteCurrentGet, name="get_deleted_note", tags=["notes"])
async def get_all_notes(token: AuthToken = Depends(check_auth_token), note_id=int, db: Session = Depends(get_db)):
    if token:
        note = db.query(Notes).filter(Notes.user_id == token.user_id, Notes.id == note_id,
                                      Notes.status_delete == True).order_by(Notes.created_at.desc()).one_or_none()
        if not note:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found deleted note")

        return note


@router.delete("/user/notes/deleted/{note_id}/", name="full_delete_note", tags=["notes"])
async def delete_note(token: AuthToken = Depends(check_auth_token), note_id=str, db: Session = Depends(get_db)):
    if token:
        db.query(Notes).where(Notes.user_id == token.user_id, Notes.id == note_id).delete()
        db.commit()

        return {f"Delete note with note_id: {note_id} was full deleted successfully"}


@router.get("/user/notes/{note_id}/", response_model=NoteCurrentGet, name="get_note", tags=["notes"])
async def get_all_notes(token: AuthToken = Depends(check_auth_token), note_id=int, db: Session = Depends(get_db)):
    if token:
        note = db.query(Notes).filter(Notes.user_id == token.user_id, Notes.id == note_id,
                                      Notes.status_delete == False).order_by(Notes.created_at.desc()).one_or_none()
        if not note:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found note")

        return note


@router.patch("/user/notes/{note_id}/", name="update_note", tags=["notes"])
async def update_note(token: AuthToken = Depends(check_auth_token), note: NoteUpdate = Body(..., embed=True),
                      note_id=int, db: Session = Depends(get_db)):
    if token:
        data = {}
        check_data = note.dict()
        for attr in check_data:
            if check_data[attr] != "":
                data[attr] = check_data[attr]
        data['updated_at'] = datetime.datetime.utcnow()

        db.query(Notes).where(Notes.user_id == token.user_id, Notes.id == note_id,
                              Notes.status_delete == False).update(values=data)
        db.commit()

        return {"Update note is successfully"}


@router.delete("/user/notes/{note_id}/", name="delete_note", tags=["notes"])
async def delete_note(token: AuthToken = Depends(check_auth_token), note_id=str, db: Session = Depends(get_db)):
    if token:
        db.query(Notes).where(Notes.user_id == token.user_id, Notes.id == note_id).\
            update(values={"status_delete": True})

        db.commit()

        return {f"Note with note_id: {note_id} was deleted successfully"}

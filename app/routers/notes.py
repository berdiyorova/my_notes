from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from app.database import get_db
from app.models import NoteModel, UserModel
from app.schemas.note import NoteIn, NoteOut
from app.security.jwt_token import get_current_active_user

router = APIRouter(
    tags=["notes"]
)

@router.post("/notes/", response_model=NoteOut, status_code=201)
async def add_note(note_in: NoteIn, current_user: Annotated[UserModel, Depends(get_current_active_user)]):
    try:
        note_in.user_id = current_user.id
        db = next(get_db())

        note = NoteModel(**note_in.dict())
        db.add(note)
        db.commit()
        db.refresh(note)
        return note
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Something went wrong")


@router.get("/notes/", status_code=200)
async def get_notes() -> list[NoteOut]:
    db = next(get_db())
    notes = db.exec(select(NoteModel)).all()
    return notes


@router.get("/notes/{note_id}", response_model=NoteOut, status_code=200)
async def get_note(note_id: int):
    db = next(get_db())
    note = db.exec(select(NoteModel).where(NoteModel.id == note_id)).one_or_none()
    if note is None:
        raise HTTPException(status_code=404, detail='Note not found')
    return note


@router.delete("/notes/{note_id}/", status_code=200)
async def delete_note(note_id: int) -> dict:
    db = next(get_db())
    note = db.get(NoteModel, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"status": True, "detail": "Note is deleted"}


@router.put("/notes/{note_id}/", status_code=200)
async def update_note(note_id: int, note_in: NoteIn) -> dict:
    db = next(get_db())
    note = db.exec(select(NoteModel).where(NoteModel.id == note_id)).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = note_in.title
    note.content = note_in.content
    note.user_id = note_in.user_id

    db.commit()
    return note

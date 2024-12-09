from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    content: str
    user_id: int | None = Field(default=None)


class NoteOut(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=255)
    content: str
    user_id: int

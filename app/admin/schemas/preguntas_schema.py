from pydantic import BaseModel
from typing import List, Optional


class OptionSchema(BaseModel):
    text: str
    is_correct: bool


class QuestionCreate(BaseModel):
    text: str
    difficulty_id: int
    options: List[OptionSchema]


class QuestionResponse(BaseModel):
    id: int
    text: str
    difficulty_id: int
    options: List[OptionSchema]

    class Config:
        from_attributes = True


class DifficultyCreate(BaseModel):
    name: str


class DifficultyResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class OptionCreate(BaseModel):
    text: str
    is_correct: bool


class QuestionCreate(BaseModel):
    text: str
    difficulty_id: int
    options: List[OptionCreate]


class QuestionUpdate(BaseModel):
    text: str
    difficulty_id: int
    options: List[OptionCreate]

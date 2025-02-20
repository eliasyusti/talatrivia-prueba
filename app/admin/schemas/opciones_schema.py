from pydantic import BaseModel
from typing import List


class OptionCreate(BaseModel):
    text: str
    is_correct: bool


class QuestionCreate(BaseModel):
    text: str
    difficulty_id: int
    options: List[OptionCreate]

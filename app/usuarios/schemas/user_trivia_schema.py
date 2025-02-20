from pydantic import BaseModel
from typing import List, Optional


class UserTriviaBase(BaseModel):
    """📌 Esquema base para UserTrivia (trivias respondidas por usuarios)."""

    user_id: int
    trivia_id: int
    score: int


class UserTriviaCreate(UserTriviaBase):
    """📌 Esquema para crear un registro de trivia respondida."""


class UserTriviaResponse(UserTriviaBase):
    """📌 Esquema para responder con detalles de trivias realizadas por un usuario."""

    id: int
    total_questions: int
    correct_answers: int
    incorrect_answers: int

    class Config:
        from_attributes = True

from app.admin.schemas.preguntas_schema import QuestionResponse
from pydantic import BaseModel
from typing import List, Optional


class TriviaBase(BaseModel):
    name: str
    description: Optional[str] = None


class TriviaCreate(TriviaBase):
    """Permite crear una trivia sin preguntas o con preguntas existentes."""

    question_ids: Optional[List[int]] = []


class TriviaResponse(TriviaBase):
    """Respuesta de trivia con preguntas asociadas."""

    id: int
    questions: List[QuestionResponse]

    class Config:
        from_attributes = True


class TriviaWithQuestions(TriviaBase):
    question_ids: List[int]


class TriviaCreateWithQuestions(BaseModel):
    name: str
    description: Optional[str] = None
    question_ids: List[int]

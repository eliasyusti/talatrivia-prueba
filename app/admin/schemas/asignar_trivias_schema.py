from pydantic import BaseModel
from typing import List


class AssignTriviasToUser(BaseModel):
    """📌 Esquema para asignar trivias a un usuario."""

    user_id: int
    trivia_ids: List[int]


class TriviaAssignedResponse(BaseModel):
    """📌 Esquema para devolver trivias asignadas."""

    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class UserWithAssignedTrivias(BaseModel):
    """📌 Esquema para listar usuarios con trivias asignadas."""

    id: int
    name: str
    email: str
    assigned_trivias: List[TriviaAssignedResponse]

    class Config:
        from_attributes = True

from pydantic import BaseModel


class UserAnswerBase(BaseModel):
    """📌 Esquema base para una respuesta de usuario."""

    question_id: int
    selected_option_id: int


class UserAnswerCreate(UserAnswerBase):
    """📌 Esquema para almacenar la respuesta de un usuario."""


class UserAnswerResponse(UserAnswerBase):
    """📌 Esquema para devolver una respuesta almacenada."""

    id: int

    class Config:
        from_attributes = True

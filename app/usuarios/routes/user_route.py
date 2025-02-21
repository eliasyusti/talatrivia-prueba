from typing import List
from app.auth.auth import get_current_user
from app.usuarios.controllers.user_trivia_controller import submit_trivia_answers
from app.usuarios.models.user import User
from app.usuarios.schemas.user_respuestas_schema import UserAnswerCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.settings.database import get_db
from app.usuarios.controllers.user_controller import create_user

from app.usuarios.schemas.user import UserCreate, UserResponseSinRole

user_router = APIRouter()


@user_router.post("/registrar_usuario_jugador", response_model=UserResponseSinRole)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@user_router.post("/realizar_trivia/{trivia_id}/", response_model=dict)
def submit_trivia_endpoint(
    trivia_id: int,
    answers: List[UserAnswerCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Realiza la trivia"""
    return submit_trivia_answers(trivia_id, answers, db, current_user)

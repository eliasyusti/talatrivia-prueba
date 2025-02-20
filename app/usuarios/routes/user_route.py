from typing import List
from app.auth.auth import get_current_user
from app.usuarios.controllers.user_trivia_controller import submit_trivia_answers
from app.usuarios.models.user import User
from app.usuarios.schemas.user_respuestas_schema import UserAnswerCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.settings.database import get_db
from app.usuarios.controllers.user_controller import create_user, get_users
from app.usuarios.schemas.user import UserCreate, UserResponse

user_router = APIRouter()


@user_router.post("/crear_usuario", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@user_router.get("/listar_usuarios", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)


@user_router.post("/realizar_trivia/{trivia_id}/", response_model=dict)
def submit_trivia_endpoint(
    trivia_id: int,
    answers: List[UserAnswerCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return submit_trivia_answers(trivia_id, answers, db, current_user)

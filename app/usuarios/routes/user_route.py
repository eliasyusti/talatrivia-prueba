from typing import List
from app.auth.auth import get_current_user
from app.usuarios.controllers.user_trivia_controller import submit_trivia_answers
from app.usuarios.models.user import User
from app.usuarios.schemas.user_respuestas_schema import UserAnswerCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.settings.database import get_db
from app.usuarios.controllers.user_controller import (
    create_user,
    create_user_admin,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)
from app.usuarios.schemas.user import (
    UserCreate,
    UserCreateAdmin,
    UserResponse,
    UserResponseSinRole,
    UserUpdate,
)

user_router = APIRouter()


@user_router.post("/registrar_usuario_jugador", response_model=UserResponseSinRole)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@user_router.post("/crear_usuario_admin", response_model=dict)
def register_user_admin(
    user: UserCreateAdmin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crea un usuario con rol Admin o User. Solo **Admins** pueden usar esta función.
    """
    return create_user_admin(user, db, current_user)


@user_router.get("/listar_usuarios", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Solo Admins pueden listar
):
    """
    Obtiene la lista de usuarios (Solo **Admins**).
    """
    return get_users(db, current_user)


@user_router.post("/realizar_trivia/{trivia_id}/", response_model=dict)
def submit_trivia_endpoint(
    trivia_id: int,
    answers: List[UserAnswerCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Realiza la trivia"""
    return submit_trivia_answers(trivia_id, answers, db, current_user)


@user_router.get("/usuario_by_id/{user_id}", response_model=UserResponse)
def get_user_by_id_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene un usuario por su ID (Solo **Admins**).
    """
    return get_user_by_id(user_id, db, current_user)


@user_router.put("/actualizar_usuario/{user_id}", response_model=dict)
def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Actualiza los datos de un usuario (Solo **Admins**).
    """
    return update_user(user_id, user_data, db, current_user)


@user_router.delete("/eliminar_usuario/{user_id}", response_model=dict)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Elimina un usuario (Solo **Admins**).
    """
    return delete_user(user_id, db, current_user)

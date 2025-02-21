from app.admin.controllers.gestionar_usuarios_controller import *
from app.admin.schemas.gestionar_usuarios_schema import *
from app.auth.auth import get_current_user
from app.usuarios.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.settings.database import get_db

gestionar_usuarios = APIRouter()


@gestionar_usuarios.post("/crear_usuario_admin", response_model=dict)
def register_user_admin(
    user: UserCreateAdmin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crea un usuario con rol Admin o User. Solo **Admins** pueden usar esta función.
    """
    return create_user_admin(user, db, current_user)


@gestionar_usuarios.get("/listar_usuarios", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene la lista de usuarios (Solo **Admins**).
    """
    return get_users(db, current_user)


@gestionar_usuarios.get("/usuario_by_id/{user_id}", response_model=UserResponse)
def get_user_by_id_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene un usuario por su ID (Solo **Admins**).
    """
    return get_user_by_id(user_id, db, current_user)


@gestionar_usuarios.put("/actualizar_usuario/{user_id}", response_model=dict)
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


@gestionar_usuarios.delete("/eliminar_usuario/{user_id}", response_model=dict)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Elimina un usuario (Solo **Admins**).
    """
    return delete_user(user_id, db, current_user)

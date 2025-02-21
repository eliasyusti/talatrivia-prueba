from app.admin.controllers.asignar_trivias_controller import (
    assign_trivias_to_user,
    get_user_assigned_trivias,
    list_users_with_assigned_trivias,
)
from app.admin.schemas.asignar_trivias_schema import AssignTriviasToUser
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.settings.database import get_db
from app.usuarios.models.user import User
from app.auth.auth import get_current_user

user_trivia_assignment_router = APIRouter()


@user_trivia_assignment_router.post("/admin/asignar_trivias", response_model=dict)
def assign_trivias_endpoint(
    assign_data: AssignTriviasToUser,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Asigna trivias a un usuario. Solo **Admins** pueden realizar esta acción.
    """
    return assign_trivias_to_user(assign_data, db, current_user)


@user_trivia_assignment_router.get("/user/trivias/{user_id}", response_model=dict)
def get_user_trivias_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene las trivias asignadas a un usuario.
    """
    return get_user_assigned_trivias(user_id, db, current_user)


@user_trivia_assignment_router.get("/admin/users_trivias", response_model=list)
def list_users_with_trivias_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lista todos los usuarios con sus trivias asignadas. Solo **Admins** pueden ver esto.
    """
    return list_users_with_assigned_trivias(db, current_user)

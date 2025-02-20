from app.admin.controllers.user_estadisticas import (
    get_user_performance,
    list_all_users_with_scores,
)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.settings.database import get_db
from app.auth.auth import get_current_user
from app.usuarios.models.user import User

estadisticas_router = APIRouter()


@estadisticas_router.get("/rendimiento/{user_id}", response_model=dict)
def get_user_performance_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene el rendimiento de un usuario en todas las trivias que ha completado.
    Solo los **Admins** pueden acceder a esta información.
    """
    return get_user_performance(user_id, db, current_user)


@estadisticas_router.get("/ranking", response_model=List[dict])
def list_all_users_with_scores_endpoint(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Obtiene un listado de todos los usuarios con su puntaje total en trivias.
    Solo los **Admins** pueden acceder a esta información.
    """
    return list_all_users_with_scores(db, current_user)

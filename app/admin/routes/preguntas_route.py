from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.admin.controllers.preguntas_controller import (
    create_question_with_options,
    delete_question,
    list_questions,
    get_question_by_id,
    update_question,
)
from app.admin.schemas.preguntas_schema import QuestionCreate, QuestionUpdate
from app.settings.database import get_db
from app.auth.auth import get_current_user
from app.usuarios.models.user import User

question_router = APIRouter()


@question_router.post("/Rs_preguntas")
def create_question_endpoint(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    authorization: str = Header(None),
    current_user: User = Depends(get_current_user),
):
    # Validar si se proporcionó un token en la cabecera
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
        )

    # Extraer el token del encabezado
    token = authorization.split("Bearer ")[-1]

    # Validar si el usuario tiene rol Admin
    if current_user.role.name != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear preguntas",
        )

    return create_question_with_options(question_data, db, token)


@question_router.delete("/Rs_preguntas/{question_id}")
def delete_question_endpoint(
    question_id: int,
    db: Session = Depends(get_db),
    authorization: str = Header(None),
    current_user: User = Depends(get_current_user),
):
    # Validar si se proporcionó un token en la cabecera
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
        )

    # Extraer el token del encabezado
    token = authorization.split("Bearer ")[-1]

    # Validar si el usuario tiene rol Admin
    if current_user.role.name != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar preguntas",
        )

    return delete_question(question_id, db, token)


@question_router.get("/Rs_preguntas")
def list_questions_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_questions(db)


@question_router.get("/Rs_preguntas/{question_id}")
def get_question_by_id_endpoint(
    question_id: int,
    db: Session = Depends(get_db),
):
    return get_question_by_id(question_id, db)


@question_router.put("/Rs_preguntas/{question_id}")
def update_question_endpoint(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    authorization: str = Header(None),
    current_user: User = Depends(get_current_user),
):
    # Validar si se proporcionó un token en la cabecera
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
        )

    # Extraer el token del encabezado
    token = authorization.split("Bearer ")[-1]

    # Validar si el usuario tiene rol Admin
    if current_user.role.name != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar preguntas",
        )

    return update_question(question_id, question_data, db, token)

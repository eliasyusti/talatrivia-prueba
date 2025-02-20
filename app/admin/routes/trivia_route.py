from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.settings.database import get_db
from app.admin.controllers.trivias_controller import *
from app.admin.schemas.trivia_schema import (
    TriviaCreate,
    TriviaWithQuestions,
    TriviaResponse,
)
from app.auth.auth import get_current_user
from app.usuarios.models.user import User

trivia_router = APIRouter()


@trivia_router.post("/", response_model=dict)
def create_trivia_endpoint(
    trivia_data: TriviaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crea una trivia sin preguntas asociadas. Solo **Admins** pueden usar esta función.
    """
    return create_trivia(trivia_data, db, current_user)


@trivia_router.post("/with-questions", response_model=dict)
def create_trivia_with_questions_endpoint(
    trivia_data: TriviaWithQuestions,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crea una trivia y le asocia preguntas ya existentes mediante sus IDs. Solo **Admins** pueden usar esta función.
    """
    return create_trivia_with_questions(trivia_data, db, current_user)


@trivia_router.put("/{trivia_id}/add-questions", response_model=dict)
def update_trivia_add_questions_endpoint(
    trivia_id: int,
    question_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Agrega preguntas ya existentes a una trivia existente. Solo **Admins** pueden usar esta función.
    """
    return update_trivia_add_questions(trivia_id, question_ids, db, current_user)


@trivia_router.put("/{trivia_id}", response_model=dict)
def update_trivia_endpoint(
    trivia_id: int,
    trivia_data: TriviaCreateWithQuestions,  # Ahora recibe el esquema completo
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Actualiza completamente una trivia: nombre, descripción y preguntas asociadas.
    Solo **Admins** pueden usar esta función.
    """
    return update_trivia(trivia_id, trivia_data, db, current_user)


@trivia_router.delete("/{trivia_id}", response_model=dict)
def delete_trivia_endpoint(
    trivia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Elimina una trivia. Solo **Admins** pueden usar esta función.
    """
    return delete_trivia(trivia_id, db, current_user)


@trivia_router.get("/", response_model=List[TriviaResponse])
def list_all_trivias_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene todas las trivias disponibles (solo para Admins).
    """
    return list_all_trivias(db, current_user)


@trivia_router.get("/{trivia_id}", response_model=TriviaResponse)
def get_trivia_by_id_endpoint(
    trivia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene una trivia específica por su ID (solo para Admins).
    """
    return get_trivia_by_id(trivia_id, db, current_user)

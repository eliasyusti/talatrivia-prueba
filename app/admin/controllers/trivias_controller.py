from app.admin.models.preguntas_model import Question
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from app.admin.models.trivia_model import Trivia
from app.admin.models.trivia_model import trivia_questions
from app.admin.schemas.trivia_schema import *
from app.auth.auth import check_admin, get_current_user
from app.usuarios.models.user import User


def create_trivia(
    trivia_data: TriviaCreate,
    db: Session,
    current_user: User = Depends(get_current_user),
):
    """
    Crea una trivia sin preguntas asociadas (solo para Admins).
    """
    check_admin(current_user)

    new_trivia = Trivia(name=trivia_data.name, description=trivia_data.description)
    db.add(new_trivia)
    db.commit()
    db.refresh(new_trivia)

    return {"message": "Trivia creada exitosamente", "trivia_id": new_trivia.id}


def create_trivia_with_questions(
    trivia_data: TriviaWithQuestions,
    db: Session,
    current_user: User = Depends(get_current_user),
):
    """
    Crea una trivia y le asocia preguntas ya existentes mediante sus IDs (solo para Admins).
    """
    check_admin(current_user)

    new_trivia = Trivia(name=trivia_data.name, description=trivia_data.description)
    db.add(new_trivia)
    db.commit()
    db.refresh(new_trivia)

    questions = db.query(Trivia).filter(Trivia.id.in_(trivia_data.question_ids)).all()

    if len(questions) != len(trivia_data.question_ids):
        raise HTTPException(
            status_code=400, detail="Uno o más IDs de preguntas no existen"
        )

    for question in questions:
        db.execute(
            trivia_questions.insert().values(
                trivia_id=new_trivia.id, question_id=question.id
            )
        )

    db.commit()

    return {"message": "Trivia creada con preguntas", "trivia_id": new_trivia.id}


def update_trivia_add_questions(
    trivia_id: int,
    question_ids: list[int],
    db: Session,
    current_user: User = Depends(get_current_user),
):
    """
    Actualiza una trivia agregándole preguntas mediante sus IDs (solo para Admins).
    """
    check_admin(current_user)

    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(status_code=404, detail="Trivia no encontrada")

    questions = db.query(Trivia).filter(Trivia.id.in_(question_ids)).all()

    if len(questions) != len(question_ids):
        raise HTTPException(
            status_code=400, detail="Uno o más IDs de preguntas no existen"
        )

    for question in questions:
        db.execute(
            trivia_questions.insert().values(
                trivia_id=trivia.id, question_id=question.id
            )
        )

    db.commit()

    return {
        "message": "Trivia actualizada con nuevas preguntas",
        "trivia_id": trivia.id,
    }


def delete_trivia(
    trivia_id: int, db: Session, current_user: User = Depends(get_current_user)
):
    """
    Elimina una trivia (solo para Admins).
    """
    check_admin(current_user)

    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(status_code=404, detail="Trivia no encontrada")

    db.delete(trivia)
    db.commit()

    return {"message": "Trivia eliminada exitosamente"}


def list_all_trivias(db: Session, current_user: User = Depends(get_current_user)):
    """
    Obtiene todas las trivias disponibles (solo para Admins).
    """
    check_admin(current_user)
    trivias = db.query(Trivia).all()
    return trivias


def get_trivia_by_id(
    trivia_id: int, db: Session, current_user: User = Depends(get_current_user)
):
    """
    Obtiene una trivia específica por su ID (solo para Admins).
    """
    check_admin(current_user)

    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(status_code=404, detail="Trivia no encontrada")

    return trivia


def update_trivia(
    trivia_id: int,
    trivia_data: TriviaCreateWithQuestions,
    db: Session,
    current_user: User = Depends(get_current_user),
):
    """
    Actualiza completamente una trivia, incluyendo su nombre, descripción y preguntas asociadas (solo para Admins).
    """
    check_admin(current_user)

    # Verificar si la trivia existe
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(status_code=404, detail="Trivia no encontrada")

    # Actualizar los datos básicos
    trivia.name = trivia_data.name
    trivia.description = trivia_data.description

    # Verificar que todas las preguntas existen
    questions = (
        db.query(Question).filter(Question.id.in_(trivia_data.question_ids)).all()
    )
    if len(questions) != len(trivia_data.question_ids):
        raise HTTPException(
            status_code=400, detail="Uno o más IDs de preguntas no existen"
        )

    # Limpiar preguntas actuales y agregar las nuevas
    db.execute(
        trivia_questions.delete().where(trivia_questions.c.trivia_id == trivia.id)
    )
    for question in questions:
        db.execute(
            trivia_questions.insert().values(
                trivia_id=trivia.id, question_id=question.id
            )
        )

    # Guardar cambios
    db.commit()
    db.refresh(trivia)

    return {
        "message": "Trivia actualizada correctamente",
        "trivia_id": trivia.id,
    }

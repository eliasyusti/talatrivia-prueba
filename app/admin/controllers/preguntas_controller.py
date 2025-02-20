from app.admin.models.opciones_model import Option
from app.admin.models.preguntas_model import Question
from app.admin.schemas.preguntas_schema import QuestionCreate, QuestionUpdate
from app.usuarios.models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.auth.auth import decode_token


def create_question_with_options(
    question_data: QuestionCreate, db: Session, token: str
):
    # Decodificar el token para obtener el usuario autenticado
    user_email = decode_token(token)

    if not user_email:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    # Buscar el usuario en la base de datos
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Verificar si el usuario tiene el rol 'Admin'
    if user.role.name != "Admin":
        raise HTTPException(
            status_code=403, detail="No tienes permisos para crear preguntas"
        )

    # Crear la pregunta
    question = Question(
        text=question_data.text, difficulty_id=question_data.difficulty_id
    )
    db.add(question)
    db.commit()
    db.refresh(question)

    # Crear las opciones
    options = [
        Option(text=opt.text, is_correct=opt.is_correct, question_id=question.id)
        for opt in question_data.options
    ]
    db.add_all(options)
    db.commit()

    return {
        "message": "Pregunta y opciones creadas exitosamente",
        "question_id": question.id,
    }


def delete_question(question_id: int, db: Session, token: str):
    # Decodificar el token para obtener el usuario autenticado
    user_email = decode_token(token)

    if not user_email:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    # Buscar el usuario en la base de datos
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Verificar si el usuario tiene el rol 'Admin'
    if user.role.name != "Admin":
        raise HTTPException(
            status_code=403, detail="No tienes permisos para eliminar preguntas"
        )

    # Buscar la pregunta en la base de datos
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    # Eliminar las opciones asociadas
    db.query(Option).filter(Option.question_id == question_id).delete()

    # Eliminar la pregunta
    db.delete(question)
    db.commit()

    return {"message": "Pregunta y opciones eliminadas exitosamente"}


def list_questions(db: Session):
    questions = db.query(Question).all()
    return questions


def get_question_by_id(question_id: int, db: Session):
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    options = db.query(Option).filter(Option.question_id == question_id).all()
    difficulty = question.difficulty

    return {
        "question": question,
        "options": options,
        "difficulty": difficulty,
    }


def update_question(
    question_id: int, question_data: QuestionUpdate, db: Session, token: str
):
    # Decodificar el token para obtener el usuario autenticado
    user_email = decode_token(token)

    if not user_email:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    # Buscar el usuario en la base de datos
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Verificar si el usuario tiene el rol 'Admin'
    if user.role.name != "Admin":
        raise HTTPException(
            status_code=403, detail="No tienes permisos para actualizar preguntas"
        )

    # Buscar la pregunta en la base de datos
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    # Actualizar la pregunta
    question.text = question_data.text
    question.difficulty_id = question_data.difficulty_id
    db.commit()
    db.refresh(question)

    # Actualizar las opciones
    db.query(Option).filter(Option.question_id == question_id).delete()
    options = [
        Option(text=opt.text, is_correct=opt.is_correct, question_id=question.id)
        for opt in question_data.options
    ]
    db.add_all(options)
    db.commit()

    return {
        "message": "Pregunta y opciones actualizadas exitosamente",
        "question_id": question.id,
    }

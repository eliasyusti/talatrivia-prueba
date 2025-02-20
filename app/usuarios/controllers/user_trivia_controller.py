from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, Depends
from app.admin.models.opciones_model import Option
from app.usuarios.models.user_respuestas_model import UserAnswer
from app.usuarios.schemas.user_respuestas_schema import UserAnswerCreate
from app.admin.models.trivia_model import Trivia
from app.admin.models.preguntas_model import Question
from app.usuarios.models.user import User
from app.usuarios.models.user_trivia_model import UserTrivia
from app.auth.auth import get_current_user

# Puntos por dificultad
DIFFICULTY_SCORES = {1: 1, 2: 2, 3: 3}  # Fácil: 1, Medio: 2, Difícil: 3


def submit_trivia_answers(
    trivia_id: int,
    answers: list[UserAnswerCreate],
    db: Session,
    current_user: User = Depends(get_current_user),
):
    print(f"Usuario autenticado: {current_user.id} - {current_user.email}")

    # Verificar si la trivia existe
    trivia = (
        db.query(Trivia)
        .options(joinedload(Trivia.questions))
        .filter(Trivia.id == trivia_id)
        .first()
    )
    if not trivia:
        raise HTTPException(status_code=404, detail="Trivia no encontrada")

    print(f"Trivia encontrada: {trivia.id} - {trivia.name}")

    # Verificar si el usuario ya ha respondido esta trivia
    existing_trivia = (
        db.query(UserTrivia)
        .filter(
            UserTrivia.user_id == current_user.id, UserTrivia.trivia_id == trivia_id
        )
        .first()
    )
    if existing_trivia:
        raise HTTPException(
            status_code=400, detail="Ya has respondido esta trivia anteriormente"
        )

    # Obtener los IDs de las preguntas asociadas a la trivia
    trivia_question_ids = {q.id for q in trivia.questions}
    print(f"Preguntas asociadas a la trivia: {trivia_question_ids}")

    total_score = 0
    correct_answers = 0
    incorrect_answers = 0

    for answer in answers:
        print(
            f"Evaluando respuesta: Pregunta {answer.question_id}, Opción {answer.selected_option_id}"
        )

        # Verificar que la pregunta pertenezca a la trivia
        if answer.question_id not in trivia_question_ids:
            raise HTTPException(
                status_code=400,
                detail=f"La pregunta {answer.question_id} no pertenece a esta trivia",
            )

        # Obtener la opción seleccionada
        selected_option = (
            db.query(Option).filter(Option.id == answer.selected_option_id).first()
        )
        if not selected_option:
            raise HTTPException(
                status_code=400,
                detail=f"La opción {answer.selected_option_id} no existe",
            )

        print(
            f"Opción seleccionada encontrada: {selected_option.text} - Correcta: {selected_option.is_correct}"
        )

        is_correct = selected_option.is_correct
        if is_correct:
            correct_answers += 1
            total_score += DIFFICULTY_SCORES.get(
                db.query(Question)
                .filter(Question.id == answer.question_id)
                .first()
                .difficulty_id,
                0,
            )
        else:
            incorrect_answers += 1

        # Guardar la respuesta del usuario
        user_answer = UserAnswer(
            user_id=current_user.id,
            trivia_id=trivia_id,
            question_id=answer.question_id,
            selected_option_id=answer.selected_option_id,
            is_correct=is_correct,
        )
        db.add(user_answer)

    # Registrar que el usuario completó la trivia
    user_trivia = UserTrivia(
        user_id=current_user.id,
        trivia_id=trivia_id,
        score=total_score,
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers,
    )
    db.add(user_trivia)

    db.commit()

    print(f"Trivia completada: {trivia.name}")
    print(
        f"Puntaje final: {total_score}, Correctas: {correct_answers}, Incorrectas: {incorrect_answers}"
    )

    return {
        "message": "Trivia completada exitosamente",
        "trivia_name": trivia.name,
    }

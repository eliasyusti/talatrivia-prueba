from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, Depends
from app.usuarios.models.user_trivia_model import UserTrivia
from app.usuarios.models.user_respuestas_model import UserAnswer
from app.usuarios.models.user import User
from app.admin.models.preguntas_model import Question
from app.admin.models.opciones_model import Option
from app.auth.auth import check_admin, get_current_user


def get_user_performance(
    user_id: int, db: Session, current_user: User = Depends(get_current_user)
):
    """
    Obtiene el rendimiento de un usuario en todas las trivias que ha completado.
    Solo los Admins pueden acceder a esta información.
    """
    check_admin(current_user)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener todas las trivias que el usuario ha completado
    user_trivias = (
        db.query(UserTrivia)
        .options(joinedload(UserTrivia.trivia))
        .filter(UserTrivia.user_id == user_id)
        .all()
    )

    if not user_trivias:
        raise HTTPException(
            status_code=404, detail="El usuario no ha completado ninguna trivia"
        )

    user_data = {
        "user_id": user.id,
        "user_name": user.name,
        "trivias": [],
    }

    for user_trivia in user_trivias:
        # Obtener todas las respuestas del usuario en esta trivia
        answers = (
            db.query(UserAnswer)
            .options(joinedload(UserAnswer.question).joinedload(Question.options))
            .filter(
                UserAnswer.user_id == user_id,
                UserAnswer.trivia_id == user_trivia.trivia_id,
            )
            .all()
        )

        trivia_info = {
            "trivia_id": user_trivia.trivia_id,
            "trivia_name": user_trivia.trivia.name,
            "score": user_trivia.score,
            "correct_answers": user_trivia.correct_answers,
            "incorrect_answers": user_trivia.incorrect_answers,
            "answers": [],
        }

        for answer in answers:
            selected_option = (
                db.query(Option).filter(Option.id == answer.selected_option_id).first()
            )

            trivia_info["answers"].append(
                {
                    "question_id": answer.question.id,
                    "question_text": answer.question.text,
                    "selected_option": (
                        selected_option.text if selected_option else "N/A"
                    ),
                    "is_correct": answer.is_correct,
                }
            )

        user_data["trivias"].append(trivia_info)

    return user_data


def list_all_users_with_scores(
    db: Session, current_user: User = Depends(get_current_user)
):
    """
    Obtiene un listado de todos los usuarios con su puntaje total en trivias.
    Solo los Admins pueden acceder a esta información.
    """
    check_admin(current_user)

    users = db.query(User).outerjoin(UserTrivia).group_by(User.id).all()

    user_scores = [
        {
            "user_id": user.id,
            "user_name": user.name,
            "total_score": sum(trivia.score for trivia in user.user_trivias),
        }
        for user in users
    ]

    return user_scores

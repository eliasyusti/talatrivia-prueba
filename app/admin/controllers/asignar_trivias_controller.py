from app.admin.models.asignar_trivias_model import UserTriviaAssignment
from app.admin.schemas.asignar_trivias_schema import (
    AssignTriviasToUser,
    TriviaAssignedResponse,
    UserWithAssignedTrivias,
)
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, Depends
from app.usuarios.models.user import User
from app.admin.models.trivia_model import Trivia
from app.auth.auth import get_current_user, check_admin


def assign_trivias_to_user(
    assign_data: AssignTriviasToUser,
    db: Session,
    current_user: User = Depends(get_current_user),
):
    """
    Asigna trivias a un usuario. Solo los Admins pueden asignar trivias.
    """
    check_admin(current_user)

    user = db.query(User).filter(User.id == assign_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar que las trivias existen
    trivias = db.query(Trivia).filter(Trivia.id.in_(assign_data.trivia_ids)).all()
    if len(trivias) != len(assign_data.trivia_ids):
        raise HTTPException(
            status_code=400, detail="Uno o más IDs de trivias no existen"
        )

    # Limpiar asignaciones previas
    db.query(UserTriviaAssignment).filter(
        UserTriviaAssignment.user_id == user.id
    ).delete()

    # Crear nuevas asignaciones
    for trivia in trivias:
        assignment = UserTriviaAssignment(user_id=user.id, trivia_id=trivia.id)
        db.add(assignment)

    db.commit()
    return {"message": "Trivias asignadas correctamente"}


def get_user_assigned_trivias(
    user_id: int, db: Session, current_user: User = Depends(get_current_user)
):
    """
    Obtiene las trivias asignadas a un usuario.
    """
    user = (
        db.query(User)
        .options(joinedload(User.trivia_assignments))
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    assigned_trivias = [
        TriviaAssignedResponse(
            id=assignment.trivia.id,
            name=assignment.trivia.name,
            description=assignment.trivia.description,
        )
        for assignment in user.trivia_assignments
    ]

    return {
        "user_id": user.id,
        "user_name": user.name,
        "assigned_trivias": assigned_trivias,
    }


def list_users_with_assigned_trivias(
    db: Session, current_user: User = Depends(get_current_user)
):
    """
    Lista todos los usuarios con sus trivias asignadas.
    """
    check_admin(current_user)

    users = db.query(User).options(joinedload(User.trivia_assignments)).all()

    response = []
    for user in users:
        assigned_trivias = [
            TriviaAssignedResponse(
                id=assignment.trivia.id,
                name=assignment.trivia.name,
                description=assignment.trivia.description,
            )
            for assignment in user.trivia_assignments
        ]
        response.append(
            UserWithAssignedTrivias(
                id=user.id,
                name=user.name,
                email=user.email,
                assigned_trivias=assigned_trivias,
            )
        )

    return response

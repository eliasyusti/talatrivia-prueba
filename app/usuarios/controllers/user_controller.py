from app.auth.auth import hash_password
from app.usuarios.models.user import User, Role
from app.usuarios.schemas.user import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import HTTPException


def create_user(user: UserCreate, db: Session):
    # Verificar si el usuario ya existe
    result = db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Buscar el rol "User"
    role_result = db.execute(select(Role).filter(Role.name == "User"))
    user_role = role_result.scalars().first()
    if not user_role:
        raise HTTPException(
            status_code=500,
            detail="El rol 'User' no está configurado en la base de datos",
        )

    # Crear el usuario con contraseña hasheada y asignarle el rol "User"
    hashed_pwd = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pwd,
        role_id=user_role.id,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_users(db: Session):
    result = db.execute(select(User))
    return result.scalars().all()

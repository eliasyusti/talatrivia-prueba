from app.auth.auth import check_admin, get_current_user, hash_password
from app.usuarios.models.user import User, Role
from app.usuarios.schemas.user import UserCreate, UserCreateAdmin, UserUpdate
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import HTTPException, Depends


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


def get_users(db: Session, current_user: User = Depends(get_current_user)):
    """
    Obtiene la lista de todos los usuarios con sus roles. Solo **Admins** pueden acceder a esta información.
    """
    check_admin(current_user)

    users = (
        db.query(User.id, User.name, User.email, Role.name.label("role"))
        .join(Role, User.role_id == Role.id)
        .all()
    )

    return [
        {"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users
    ]


def get_user_by_id(
    user_id: int, db: Session, current_user: User = Depends(get_current_user)
):
    """
    Obtiene un usuario por su ID con su rol. Solo **Admins** pueden acceder a esta información.
    """
    check_admin(current_user)

    user = (
        db.query(User.id, User.name, User.email, Role.name.label("role"))
        .join(Role, User.role_id == Role.id)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}


def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session,
    current_user: User = Depends(get_current_user),
):
    """
    Actualiza la información de un usuario. Solo **Admins** pueden modificar usuarios.
    """
    check_admin(current_user)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar los datos del usuario
    if user_data.name:
        user.name = user_data.name
    if user_data.email:
        user.email = user_data.email
    if user_data.password:
        user.hashed_password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)
    return {"message": "Usuario actualizado exitosamente", "user_id": user.id}


def delete_user(
    user_id: int, db: Session, current_user: User = Depends(get_current_user)
):
    """
    Elimina un usuario. Solo **Admins** pueden eliminar usuarios.
    """
    check_admin(current_user)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()

    return {"message": "Usuario eliminado exitosamente"}


def create_user_admin(
    user: UserCreateAdmin, db: Session, current_user: User = Depends(get_current_user)
):
    """
    Crea un usuario con rol Admin o User. Solo **Admins** pueden ejecutar esta acción.
    """
    # Verificar si el usuario actual es Admin
    check_admin(current_user)

    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Buscar el rol en la base de datos
    role = db.query(Role).filter(Role.name == user.role).first()
    if not role:
        raise HTTPException(status_code=400, detail="Rol no válido")

    # Crear el usuario con la contraseña hasheada y rol asignado
    hashed_pwd = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pwd,
        role_id=role.id,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": f"Usuario {user.role} creado exitosamente",
        "user_id": new_user.id,
    }

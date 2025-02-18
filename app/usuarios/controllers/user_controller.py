from app.auth.auth import hash_password
from app.usuarios.models.user import User
from app.usuarios.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException


async def create_user(user: UserCreate, db: AsyncSession):
    # Verificar si el usuario ya existe
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Crear el usuario con contraseña hasheada
    hashed_pwd = await hash_password(user.password)
    new_user = User(name=user.name, email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)

    # Hacer commit antes de refrescar los datos
    await db.commit()

    # Refrescar el objeto para asegurar que se reflejen los cambios
    await db.refresh(new_user)

    return new_user


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

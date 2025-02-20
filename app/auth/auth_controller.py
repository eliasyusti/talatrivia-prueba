from app.auth.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.usuarios.models.user import User
from app.usuarios.schemas.user import LoginRequest, RefreshTokenRequest
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session


def login(request: LoginRequest, db: Session):
    with db.begin():
        result = db.execute(select(User).filter(User.email == request.email))
        user = result.scalars().first()

        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        access_token = create_access_token({"sub": user.email})
        refresh_token = create_refresh_token({"sub": user.email})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }


def refresh_access_token(request: RefreshTokenRequest):
    # Decodificar el refresh token
    email = decode_token(request.refresh_token)

    # Si el token es inválido, devolver error
    if email is None:
        raise HTTPException(status_code=401, detail="Refresh Token inválido o expirado")

    # Generar un nuevo Access Token
    new_access_token = create_access_token({"sub": email})

    # Devuelve también el refresh_token original
    return {
        "access_token": new_access_token,
        "refresh_token": request.refresh_token,  # 🔹 Se devuelve para cumplir con el esquema
        "token_type": "bearer",
    }

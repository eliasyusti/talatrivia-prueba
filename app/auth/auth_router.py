from typing import Annotated
from fastapi import APIRouter, Depends
from app.auth.auth_controller import login, refresh_access_token
from app.settings.database import get_db
from app.usuarios.schemas.user import LoginRequest, RefreshTokenRequest, Token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter()


@auth_router.post("/refresh", response_model=Token)
def refresh_token_endpoint(request: RefreshTokenRequest):
    return refresh_access_token(request)


@auth_router.post("/login", response_model=Token)
def login_user(
    formData: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    request = LoginRequest(email=formData.username, password=formData.password)
    return login(request, db)

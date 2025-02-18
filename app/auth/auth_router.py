from fastapi import APIRouter, Depends
from app.auth.auth_controller import login, refresh_access_token
from app.settings.database import get_db
from app.usuarios.schemas.user import LoginRequest, RefreshTokenRequest, Token
from sqlalchemy.ext.asyncio import AsyncSession


auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login_user(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login(request, db)


@auth_router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(request: RefreshTokenRequest):
    return await refresh_access_token(request)

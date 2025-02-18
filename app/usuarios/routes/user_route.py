from fastapi import APIRouter, Depends
from app.settings.database import get_db
from app.usuarios.controllers.user_controller import create_user, get_users
from app.usuarios.schemas.user import UserCreate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter()


@user_router.post("/Rs_crear_usuario", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(user, db)


@user_router.get("/Rs_listar_usuarios", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)

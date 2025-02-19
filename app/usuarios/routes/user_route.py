from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.settings.database import get_db
from app.usuarios.controllers.user_controller import create_user, get_users
from app.usuarios.schemas.user import UserCreate, UserResponse

user_router = APIRouter()


@user_router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@user_router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

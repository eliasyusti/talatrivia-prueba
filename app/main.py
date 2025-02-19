from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.routes import router
from app.usuarios.routes.user_route import user_router
from app.auth.auth_router import auth_router
from app.settings.database import Base, engine

from sqlalchemy.orm import Session

# Crear la aplicación FastAPI
app = FastAPI(
    title="FastAPI | Docker | Trivia",
    description="Talatrivia",
    version="0.0.1",
    contact={
        "name": "Elias Yusti",
        "email": "eliasyusti@gmail.com",
    },
    openapi_tags=[
        {
            "name": "Talatrivia",
        },
    ],
)


def create_tables():
    """Crea las tablas en la base de datos de manera síncrona."""
    with engine.connect() as conn:
        Base.metadata.create_all(bind=engine)


# Ejecutar la creación de tablas al iniciar la aplicación
@app.on_event("startup")
def startup():
    create_tables()


# Incluir los routers
app.include_router(router)
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.settings.data_inicial import (
    create_tables,
    seed_difficulties,
    seed_roles_and_admin,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.usuarios.routes.user_route import user_router
from app.auth.auth_router import auth_router
from app.admin.routes.preguntas_route import question_router
from app.admin.routes.trivia_route import (
    trivia_router,
)
from app.admin.routes.estadisticas_route import estadisticas_router


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


@app.on_event("startup")
def startup():
    create_tables()
    seed_roles_and_admin()
    seed_difficulties()


# Incluir los routers

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(question_router, prefix="/admin", tags=["Admin"])
app.include_router(trivia_router, prefix="/trivias", tags=["Trivias"])
app.include_router(estadisticas_router, prefix="/estadisticas", tags=["Estadisticas"])

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

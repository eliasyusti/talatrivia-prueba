from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.usuarios.routes.user_route import user_router
from app.auth.auth_router import auth_router
from app.settings.database import Base, engine

app = FastAPI()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Ejecutar la creación de tablas al iniciar la aplicación
@app.on_event("startup")
async def startup():
    await create_tables()


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

app.include_router(router)
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

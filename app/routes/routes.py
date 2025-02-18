from fastapi import APIRouter
from app.controllers.controller import helloworld_controller

router = APIRouter()


@router.get("/hello")
async def helloworld_route():
    return await helloworld_controller()

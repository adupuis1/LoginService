from app.api.routes import login, users
from fastapi import APIRouter

from app.api.routes import utils

api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(utils.router)
api_router.include_router(users.router)
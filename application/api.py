from fastapi import FastAPI
from src.routers import user, auth


def create_api():
    api = FastAPI()
    api.include_router(user.router)
    api.include_router(auth.router)
    return api

from fastapi import FastAPI
from src.routers import user


def create_api():
    api = FastAPI()
    api.include_router(user.router)
    return api

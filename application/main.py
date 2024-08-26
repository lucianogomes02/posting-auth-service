from fastapi import FastAPI

from application.db_config import mongo_start_connection
from src.routers import user
from src.routers import auth

mongo_start_connection()
api = FastAPI()
api.include_router(user.router)
api.include_router(auth.router)

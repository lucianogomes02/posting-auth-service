from fastapi import FastAPI, Request

from src.routers import auth, user

api = FastAPI()


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    from application.db_config import mongo_start_connection
    from application.settings import Settings

    settings = Settings()

    mongo_start_connection(
        uri=settings.MONGO_URI,
        database=settings.MONGO_USER_DATABASE,
        username=settings.MONGO_USER,
        password=settings.MONGO_PASSWORD,
    )

    response = await call_next(request)
    return response


api.include_router(user.router)
api.include_router(auth.router)

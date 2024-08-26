import mongoengine

from application.settings import Settings

settings = Settings()


def mongo_start_connection():
    try:
        mongoengine.connect(
            db=settings.MONGO_USER_DATABASE,
            host=settings.MONGO_URI,
            username=settings.MONGO_USER,
            password=settings.MONGO_PASSWORD,
            alias="default",
        )
    except mongoengine.ConnectionFailure as e:
        raise e

import os
import mongoengine


def mongo_start_connection():
    try:
        mongoengine.connect(
            db=os.getenv("MONGO_USER_DATABASE"),
            host=os.getenv("MONGO_URI"),
            username=os.getenv("MONGO_USER"),
            password=os.getenv("MONGO_PASSWORD"),
            alias="default",
        )
    except mongoengine.ConnectionFailure as e:
        raise e

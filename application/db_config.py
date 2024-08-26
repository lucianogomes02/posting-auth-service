import mongoengine


def mongo_start_connection(uri, database, username=None, password=None):
    try:
        mongoengine.connect(
            db=database,
            host=uri,
            username=username,
            password=password,
            alias="default",
        )
    except mongoengine.ConnectionFailure as e:
        raise e

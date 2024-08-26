import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

from application.db_config import mongo_start_connection
from application.main import api
from application.security import get_password_hash
from src.models.user import User


@pytest.fixture(scope="session")
def settings():
    return {
        "MONGO_URI": "mongodb://localhost:27017/",
        "MONGO_USER_DATABASE": "test_database",
        "MONGO_USER": "",
        "MONGO_PASSWORD": "",
        "SECRET_KEY": "test_secret_key",
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": 30,
    }


@pytest.fixture(scope="function")
def engine(settings):
    with MongoDbContainer("mongo:7.0.7") as mongo:
        mongo_uri = mongo.get_connection_url()
        client = MongoClient(mongo_uri)
        db = client.get_database(settings["MONGO_USER_DATABASE"])

        mongo_start_connection(
            settings.get("MONGO_URI"),
            settings.get("MONGO_USER_DATABASE"),
            settings.get("MONGO_USER"),
            settings.get("MONGO_PASSWORD"),
        )
        yield db
        db.drop_collection("users")
        db.create_collection("users")
        for collection_name in db.list_collection_names():
            db[collection_name].delete_many({})
        client.close()


@pytest.fixture
def client(engine, monkeypatch, settings):
    for key, value in settings.items():
        monkeypatch.setenv(key, value)

    with TestClient(api) as client:
        yield client


@pytest.fixture(scope="function")
def user_test(engine):
    User.objects().delete()
    password = get_password_hash("123456")
    User.objects.create(
        name="User-Test",
        nickname="user_test",
        email="test@test.com",
        password=password,
    )
    user = User.objects(email="test@test.com").first()
    return user


@pytest.fixture(scope="function")
def token(client, user_test):
    response = client.post(
        "/auth/login",
        data={"username": user_test.email, "password": "123456"},
    )
    return response.json()["access_token"]

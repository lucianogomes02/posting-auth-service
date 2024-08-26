from datetime import datetime

from mongoengine import (
    Document,
    StringField,
    EmailField,
    BooleanField,
    DateTimeField,
)


class User(Document):
    name = StringField(required=True)
    nickname = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=512, required=True)
    is_active = BooleanField(default=True)
    created_when = DateTimeField(default=datetime.now)
    updated_when = DateTimeField(default=datetime.now)
    last_login = DateTimeField()
    deleted = BooleanField(default=False)
    deleted_when = DateTimeField()

    meta = {"collection": "users", "indexes": ["nickname", "email"]}

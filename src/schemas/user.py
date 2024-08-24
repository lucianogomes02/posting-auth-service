from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr


class ObjectIdStr(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError("ObjectId required")
        return str(v)


class UserSchema(BaseModel):
    id: ObjectIdStr
    name: str
    nickname: str
    email: EmailStr
    is_active: bool
    created_when: datetime
    updated_when: datetime
    last_login: datetime
    deleted: bool
    deleted_when: Optional[datetime] = None


class UserList(BaseModel):
    users: list[UserSchema]

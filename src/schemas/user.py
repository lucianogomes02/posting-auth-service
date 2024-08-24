from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    id: str
    name: str
    nickname: str
    email: EmailStr
    is_active: bool
    created_when: datetime
    updated_when: datetime
    last_login: datetime
    deleted: bool
    deleted_when: Optional[datetime] = None


class UserSchema(BaseModel):
    name: str
    nickname: str
    email: EmailStr
    password: str


class CreatedUser(BaseModel):
    id: str


class UserList(BaseModel):
    users: list[UserPublic]

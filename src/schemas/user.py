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
    last_login: Optional[datetime] = None
    deleted: bool = False
    deleted_when: Optional[datetime] = None

    @classmethod
    def mongo_to_pydantic(cls, document: dict) -> "UserPublic":
        return cls(
            id=str(document["_id"]),
            name=document["name"],
            nickname=document["nickname"],
            email=document["email"],
            is_active=document["is_active"],
            created_when=document["created_when"],
            updated_when=document["updated_when"],
            last_login=document.get("last_login"),
            deleted=document.get("deleted"),
            deleted_when=document.get("deleted_when"),
        )


class UserSchema(BaseModel):
    name: str
    nickname: str
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserId(BaseModel):
    id: str


class UserList(BaseModel):
    users: list[UserPublic]

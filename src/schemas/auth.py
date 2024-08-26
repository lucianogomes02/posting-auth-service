from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserAuthSchema(BaseModel):
    id: str
    name: str
    nickname: str
    email: EmailStr
    password: str
    updated_when: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    deleted: bool = False

    @classmethod
    def mongo_to_pydantic(cls, document: dict) -> Optional["UserAuthSchema"]:
        if not document:
            return None
        return cls(
            id=str(document["_id"]),
            name=document["name"],
            nickname=document["nickname"],
            password=document["password"],
            email=document["email"],
            is_active=document["is_active"],
            updated_when=document.get("updated_when", None),
            last_login=document.get("last_login", None),
        )

from datetime import datetime
from http import HTTPStatus

from bson import ObjectId
from fastapi import HTTPException
from zoneinfo import ZoneInfo

from application.security import get_password_hash
from src.repositories.user import UserRepository
from src.schemas.auth import UserAuthSchema
from src.schemas.user import UserId, UserPublic, UserSchema, UserUpdateSchema


class UserService:
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    async def get_user(self, user_id: ObjectId) -> UserPublic:
        return self.user_repository.get_user(user_id)

    def get_user_by_email(self, email: str) -> UserAuthSchema:
        return self.user_repository.get_user_by_email(email)

    async def get_users(self) -> list[UserPublic]:
        return self.user_repository.get_users()

    def create_user(self, user: UserSchema) -> UserId:
        user.password = get_password_hash(user.password)
        user_id = self.user_repository.create_user(user)
        return UserId(id=str(user_id))

    def update_user(self, params: UserUpdateSchema, user_id: ObjectId) -> UserId:
        user = self.user_repository.get_user_by_id(user_id=user_id)
        if not user or user.get("deleted", False):
            raise HTTPException(HTTPStatus.NOT_FOUND, "User not found")

        for attribute, value in params.model_dump().items():
            if value:
                user[attribute] = value

        user["updated_when"] = datetime.now(tz=ZoneInfo("UTC"))
        updated_user = self.user_repository.update_user(user)
        return UserId(id=str(updated_user))

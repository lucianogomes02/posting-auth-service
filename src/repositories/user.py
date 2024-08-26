from typing import Optional

from bson import ObjectId

from src.models.user import User
from src.schemas.auth import UserAuthSchema
from src.schemas.user import UserPublic, UserSchema, UserId


class UserRepository:
    @staticmethod
    def get_user(user_id: ObjectId) -> UserPublic:
        user = User._get_collection().find_one({"_id": user_id})
        return UserPublic.mongo_to_pydantic(user)

    @staticmethod
    def get_users() -> list[UserPublic]:
        users = list(User._get_collection().find())
        return [UserPublic.mongo_to_pydantic(user) for user in users]

    @staticmethod
    def create_user(user: UserSchema) -> ObjectId:
        user = User.objects.create(**user.model_dump())
        return user.id

    @staticmethod
    def get_user_by_email(email: str) -> UserAuthSchema:
        user = User._get_collection().find_one({"email": email})
        return UserAuthSchema.mongo_to_pydantic(user)

    @staticmethod
    def get_user_by_id(user_id: ObjectId) -> Optional[User]:
        return User._get_collection().find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def update_user(user: User) -> UserId:
        User._get_collection().update_one({"_id": user["_id"]}, {"$set": {**user}})
        return user["_id"]

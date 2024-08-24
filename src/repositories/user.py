from bson import ObjectId

from src.models.user import User
from src.schemas.user import UserSchema


class UserRepository:
    @staticmethod
    def get_user(user_id: ObjectId) -> UserSchema:
        user = User._get_collection().find_one({"_id": user_id})
        return UserSchema(**user)

    @staticmethod
    def get_users() -> list[UserSchema]:
        users = list(User._get_collection().find())
        return [UserSchema(**user) for user in users]

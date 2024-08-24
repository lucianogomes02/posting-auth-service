from bson import ObjectId

from src.models.user import User
from src.schemas.user import UserPublic, UserSchema


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
        return User.objects.create(**user.model_dump()).id

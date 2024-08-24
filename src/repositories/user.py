from bson import ObjectId

from application.security import get_password_hash
from src.models.user import User
from src.schemas.auth import UserAuthSchema
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
        user_data = {**user.model_dump()}
        user_data["password"] = get_password_hash(user.password)
        user = User.objects.create(**user_data)
        return user.id

    @staticmethod
    def get_user_by_email(email: str) -> UserAuthSchema:
        user = User._get_collection().find_one({"email": email})
        return UserAuthSchema.mongo_to_pydantic(user)

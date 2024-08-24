from bson import ObjectId

from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import UserSchema


class UserService:
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    def get_user(self, user_id: ObjectId) -> UserSchema:
        return self.user_repository.get_user(user_id)

    def get_users(self) -> list[UserSchema]:
        return self.user_repository.get_users()

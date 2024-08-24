from bson import ObjectId

from src.repositories.user import UserRepository
from src.schemas.user import UserPublic, UserSchema


class UserService:
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    async def get_user(self, user_id: ObjectId) -> UserPublic:
        return self.user_repository.get_user(user_id)

    async def get_users(self) -> list[UserPublic]:
        return self.user_repository.get_users()

    async def create_user(self, user: UserSchema) -> ObjectId:
        return self.user_repository.create_user(user)

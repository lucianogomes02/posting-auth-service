from fastapi import APIRouter

from src.schemas.user import UserList
from src.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])
user_service = UserService()


@router.get("/", response_model=UserList)
async def read_users():
    return {"users": user_service.get_users()}

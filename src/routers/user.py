from http import HTTPStatus
from http.client import HTTPException

from bson import ObjectId
from fastapi import APIRouter

from src.schemas.user import UserList, CreatedUser, UserSchema, UserPublic
from src.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])
user_service = UserService()


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
async def get_user_by_id(user_id: str):
    try:
        user = await user_service.get_user(ObjectId(user_id))
        return user
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(e))


@router.get("/", status_code=HTTPStatus.OK, response_model=UserList)
async def read_users():
    try:
        users = await user_service.get_users()
        return UserList(users=users)
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(e))


@router.post("/", status_code=HTTPStatus.CREATED, response_model=CreatedUser)
async def create_user(user: UserSchema):
    try:
        new_user = await user_service.create_user(user)
        return CreatedUser(id=str(new_user))
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(e))

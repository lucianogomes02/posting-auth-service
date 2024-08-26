from http import HTTPStatus
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends

from application.security import get_current_user
from src.models.user import User
from src.schemas.user import UserList, UserId, UserSchema, UserPublic, UserUpdateSchema
from src.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])
CurrentUser = Annotated[User, Depends(get_current_user)]

user_service = UserService()


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
async def get_user_by_id(user_id: str, current_user: CurrentUser):
    try:
        if not str(current_user.id) == user_id:
            raise HTTPException(HTTPStatus.FORBIDDEN, "You don't have permission to access this user")
        user = await user_service.get_user(ObjectId(user_id))
        return user
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(e))


@router.get("/", status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(current_user: CurrentUser):
    try:
        users = await user_service.get_users()
        return UserList(users=users)
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(e))


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserId)
def create_user(user: UserSchema):
    try:
        return user_service.create_user(user)
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(e))


@router.put("/{user_id}", status_code=HTTPStatus.OK, response_model=UserId)
def update_user(user_id: str, params: UserUpdateSchema, current_user: CurrentUser):
    try:
        if str(current_user.id) != user_id:
            raise HTTPException(HTTPStatus.FORBIDDEN, "You don't have permission to update this user")
        updated_user = user_service.update_user(params, current_user.id)
        return updated_user
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(e))

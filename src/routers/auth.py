from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from application.security import (
    verify_password,
    create_access_token,
    get_current_user,
)
from src.schemas.auth import Token, UserAuthSchema
from src.services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])
user_service = UserService()

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/login", response_model=Token)
def login(form_data: OAuth2Form):
    user = user_service.get_user_by_email(form_data.username)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Incorrect nickname or password",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Incorrect nickname or password",
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh_token", response_model=Token)
def refresh_access_token(
    user: UserAuthSchema = Depends(get_current_user),
):
    new_access_token = create_access_token(data={"sub": user.email})

    return {"access_token": new_access_token, "token_type": "bearer"}

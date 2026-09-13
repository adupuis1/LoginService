import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from app import crud
from app.api.deps import (
    CurrentUser, 
    SessionDep, 
    get_current_user
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import (
    UserPublic,
    UserCreate
)

router = APIRouter(prefix="/users", tags=["users"])



@router.post(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=UserPublic,
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:

    user = crud.get_user_by_username(session=session, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system."
        )
    user = crud.create_user(session=session, user_create=user_in)
    return user
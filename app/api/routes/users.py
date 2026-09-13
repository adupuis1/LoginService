import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from app import crud
from app.api.deps import (
    CurrentUser, 
    SessionDep, 
    get_current_user,
    get_current_active_superuser,

)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import (
    User,
    UserPublic,
    UserCreate,
    UserRegister,
)

router = APIRouter(prefix="/users", tags=["users"])


# for admins ------------------------------------------------------------------------
@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
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

# -----------------------------------------------------------------------------------

# for users -------------------------------------------------------------------------
## --- signup -----------------------------------------------------------------------
@router.post(
    "/signup",
    response_model=UserPublic
)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:

    user = crud.get_user_by_username(session=session, username = user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system"
        )
    user_create = UserCreate.model_validate(user_in)
    user = crud.create_user(session=session, user_create=user_create)
    return user

## --- get user by id --------------------------------------------------------------
@router.get(
    "/get/{user_id}", 
    response_model=UserPublic
)
def read_user_by_id(user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:

    user = session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user does not have enough privileges",
        )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user

from datetime import datetime, timedelta, UTC
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from backend.app import crud
from backend.app.api.deps import CurrentUser, SessionDep, get_current_user
from backend.app.core import security
from backend.app.core.config import settings
from backend.app.models import Message, Token, UserPublic, UserUpdate, RefreshRequest, User


router = APIRouter(tags=["login"])


def issue_tokens(session: Session, user: User) -> Token:
    access_token = security.create_access_token(
        user,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token= crud.create_refresh_token(
        session=session,
        user=user
    )
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

@router.post("/login/access-token")
def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:

    user = crud.authenticate(
        session=session,
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    return issue_tokens(session, user)

@router.post("/login/refresh")
def refresh_access_token(
    session: SessionDep,
    request_in: RefreshRequest
) -> Token:

    invalid = HTTPException(
        status_code=401,
        detail="Invalid refresh token"
    )

    db_token = crud.get_refresh_token(
        session=session,
        raw_token=request_in.refresh_token
    )
    if db_token is None:
        raise invalid
    if db_token.revoked_at is not None:
        # revoked token used again: probably stolen, log the user out everywhere
        crud.revoke_all_refresh_tokens(
            session=session,
            user_id=db_token.user_id
        )
        raise invalid
    if db_token.expires_at < datetime.now(UTC):
        raise invalid

    user = session.get(User, db_token.user_id)
    if user is None:
        raise invalid

    crud.revoke_refresh_token(
        session=session,
        db_token=db_token
    )
    return issue_tokens(session, user)

@router.post("/logout")
def logout(
    session: SessionDep, 
    request_in: RefreshRequest
) -> Message:
    db_token = crud.get_refresh_token(
        session=session,
        raw_token=request_in.refresh_token
    )
    if db_token is not None and db_token.revoked_at is None:
        crud.revoke_refresh_token(
            session=session,
            db_token=db_token
        )
    return Message(message="Logged out")
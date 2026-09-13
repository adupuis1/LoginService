import uuid
from typing import Any
from datetime import UTC, datetime, timedelta

from sqlmodel import Session, select, col
from backend.app.core.security import get_password_hash, verify_password
from backend.app.models import User, UserCreate, UserUpdate, RefreshToken
from backend.app.core import security
from backend.app.core.config import settings


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def  get_user_by_username(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user
# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    db_user = get_user_by_username(session = session, username = username)
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user


def create_refresh_token(*, session: Session, user: User) -> str:
    raw_token = security.generate_refresh_token()
    db_token = RefreshToken(
        user_id=user.id,
        token_hash=security.hash_token(raw_token),
        expires_at=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    session.add(db_token)
    session.commit()
    return raw_token

def get_refresh_token(*, session: Session, raw_token: str) -> RefreshToken | None:
    statement = select(RefreshToken).where(
        RefreshToken.token_hash == security.hash_token(raw_token)
    )
    return session.exec(statement).first()

def revoke_refresh_token(*, session: Session, db_token: RefreshToken) -> None:
    db_token.revoked_at = datetime.now(UTC)
    session.add(db_token)
    session.commit()

def revoke_all_refresh_tokens(*, session: Session, user_id) -> None:
    statement = select(RefreshToken).where(
        RefreshToken.user_id == user_id,
        col(RefreshToken.revoked_at).is_(None),
    )
    now = datetime.now(UTC)
    for db_token in session.exec(statement).all():
        db_token.revoked_at = now
        session.add(db_token)
    session.commit()
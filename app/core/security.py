from datetime import UTC, datetime, timedelta
import hashlib
import secrets
from typing import Any
from pathlib import Path

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from app.core.config import settings
from app.models import User
password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher
    )
)

ALGORITHM = "RS256"
PUBLIC_KEY = Path(settings.PUBLIC_KEY_PATH).read_text()
PRIVATE_KEY = Path(settings.PRIVATE_KEY_PATH).read_text()

def create_access_token(user: User, expires_delta: timedelta) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "is_superuser": user.is_superuser,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "iat": now,
        "exp": now + expires_delta,
    }
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.PRIVATE_KEY, 
        algorithm=ALGORITHM,
        headers={"kid": settings.JWT_KEY_ID}
    )
    return encoded_jwt

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode()).hexidigest()

def verify_password(
        plain_password: str, hashed_password: str
) -> tuple[bool, str | None]:
    return password_hash.verify_and_update(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)
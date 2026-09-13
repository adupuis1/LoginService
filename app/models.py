import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

def get_date_time_utc() -> datetime:
    return datetime.now(UTC)

class UserBase(SQLModel):
    username : str = Field(unique=True, index=True, max_length=255)
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(UserBase):
    username : str | None = Field(default=None, max_length=255)
    password : str | None = Field(default=None, max_length=255)
    is_superuser : bool | None = None

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password : str
    created_at: datetime | None = Field(
        default_factory=get_date_time_utc,
        sa_type=DateTime(timezone=True),
    )

class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None 

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


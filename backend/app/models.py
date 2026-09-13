import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

def get_date_time_utc() -> datetime:
    return datetime.now(UTC)

class UserBase(SQLModel):
    username : str = Field(unique=True, index=True, max_length=255)
    is_superuser : bool = False

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserRegister(SQLModel):
    username: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(UserBase):
    username : str | None = Field(default=None, max_length=255)
    password : str | None = Field(default=None, max_length=255)
    

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
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class RefreshRequest(SQLModel):
    refresh_token: str

# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None

class RefreshToken(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index = True)
    token_hash : str = Field(unique=True, index=True)
    expires_at: datetime = Field(sa_type=DateTime(timezone=True))
    revoked_at: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))
    created_at: datetime = Field(default_factory=get_date_time_utc, sa_type=DateTime(timezone=True))

class Message(SQLModel):
    message: str
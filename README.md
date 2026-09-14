# LoginService

A standalone authentication service that all my apps share. It handles sign-up, login, and short-lived access tokens with rotating refresh tokens. Tokens are signed with **RS256**, and the public key is published as a **JWKS**, so any other app can verify them without a shared secret and without calling this service on every request.

## Features

- Username + password sign-up and login (passwords hashed with Argon2)
- **RS256 JWT access tokens** (15 minutes) with `sub`, `username`, `is_superuser`, `iss`, `aud`, `iat`, `exp`, plus a `kid` header
- **JWKS endpoint** (`/.well-known/jwks.json`) so other apps can verify tokens locally
- **Refresh tokens** (30 days), stored only as SHA-256 hashes
  - **Rotation:** every refresh replaces the refresh token
  - **Reuse detection:** reusing an old refresh token revokes all of that user's sessions
- **Server-side logout**, which revokes the refresh token
- **Superuser flag:** admin-only routes

## Tech stack

| Area | Tools |
|---|---|
| API | FastAPI, Pydantic Settings |
| Database | PostgreSQL, SQLModel, psycopg 3 |
| Auth | PyJWT (`crypto` extra), pwdlib (Argon2 / bcrypt) |
| Tooling | uv, Python 3.14 |

## Project structure

```
LoginService/
  README.md
  backend/
    pyproject.toml  uv.lock  .python-version
    .env            (not in git)
    keys/           (not in git) private.pem, public.pem
    tests/          (not in git) jwttests.py
    app/
      main.py             FastAPI app, routers, docs URLs, validation handler
      models.py           SQLModel tables and request/response schemas
      crud.py             users, authentication, refresh tokens
      core/
        config.py         settings (read from .env)
        db.py             engine, create tables
        security.py       password hashing, JWT create/decode, refresh token helpers
      api/
        main.py           combines the routers
        deps.py           DB session, current user, superuser dependencies
        routes/
          login.py        login, refresh, logout
          users.py        signup, self, get by id, admin create
          utils.py        health check
          wellknown.py    JWKS
```

## Getting started

All commands run from `backend/`.

### 1. Prerequisites

- [uv](https://docs.astral.sh/uv/)
- PostgreSQL. The quickest option is Docker:

  ```bash
  docker run -d --name loginservice-db -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:17
  ```

- `openssl`, to generate the signing keys

### 2. Install dependencies

```bash
cd backend
uv sync
```

### 3. Generate the signing keys

```bash
mkdir -p keys
openssl genpkey -algorithm RSA -out keys/private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -in keys/private.pem -pubout -out keys/public.pem
```

> `keys/` is gitignored. Never commit `private.pem`: anyone who has it can create valid tokens for any user.

### 4. Configure (optional)

The defaults work for local development. To override them, create `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:dev@localhost:5432/postgres
JWT_ISSUER=http://localhost:8000
JWT_AUDIENCE=my-apps
```

### 5. Run

```bash
uv run fastapi dev app/main.py
```

- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/api/docs`
- OpenAPI schema: `http://127.0.0.1:8000/api/v1/openapi.json`

Tables are created automatically on startup.

## Configuration

| Setting | Default | Description |
|---|---|---|
| `PROJECT_NAME` | `Login Service` | Title shown in the API docs |
| `DATABASE_URL` | `postgresql+psycopg://postgres:dev@localhost:5432/postgres` | Postgres connection string |
| `API_V1_STR` | `/api/v1` | Prefix for all API routes |
| `PRIVATE_KEY_PATH` | `keys/private.pem` | RSA private key used to sign tokens |
| `PUBLIC_KEY_PATH` | `keys/public.pem` | RSA public key used to verify tokens and served in JWKS |
| `JWT_KEY_ID` | `2026-09` | `kid` header value; change it when rotating keys |
| `JWT_ISSUER` | `http://localhost:8000` | `iss` claim; apps must check this exact value |
| `JWT_AUDIENCE` | `my-apps` | `aud` claim; apps must check this exact value |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `30` | Refresh token lifetime |

The file paths and `.env` are relative to the folder you start the app from (`backend/`).

## API

All routes except JWKS are under `/api/v1`.

| Method | Path | Auth | Body | Returns |
|---|---|---|---|---|
| `POST` | `/users/signup` | none | JSON `{ "username", "password" }` | `UserPublic` |
| `POST` | `/login/access-token` | none | **form data** `username`, `password` | `Token` |
| `POST` | `/login/refresh` | none | JSON `{ "refresh_token" }` | `Token` (new pair) |
| `POST` | `/logout` | none | JSON `{ "refresh_token" }` | `Message` |
| `GET` | `/users/self` | Bearer | | `UserPublic` |
| `GET` | `/users/get/{user_id}` | Bearer (the same user, or a superuser) | | `UserPublic` |
| `POST` | `/users/` | Bearer (**superuser**) | JSON `{ "username", "password", "is_superuser" }` | `UserPublic` |
| `GET` | `/utils/health-check/` | none | | `true` |
| `GET` | `/.well-known/jwks.json` | none | | Public key set |

**Token response**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "Q2x5...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Status codes**

| Code | Meaning |
|---|---|
| `400` | Validation error (returned instead of FastAPI's usual 422), wrong username or password, or username already taken |
| `401` | Missing, invalid or expired access token, or an invalid refresh token |
| `403` | Logged in but not allowed (for example, not a superuser) |

### Examples

```bash
# sign up
curl -X POST http://127.0.0.1:8000/api/v1/users/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "password123"}'

# log in (form data, not JSON)
curl -X POST http://127.0.0.1:8000/api/v1/login/access-token \
  -d "username=test&password=password123"

# current user
curl http://127.0.0.1:8000/api/v1/users/self \
  -H "Authorization: Bearer <access_token>"

# refresh
curl -X POST http://127.0.0.1:8000/api/v1/login/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'
```

## How authentication works

1. **Login:** the service checks the password and signs an access token with `private.pem`. It also stores the SHA-256 hash of a new random refresh token.
2. **Requests:** clients send `Authorization: Bearer <access_token>`. Apps verify the signature with the public key from JWKS, and check `exp`, `iss` and `aud`.
3. **Expiry:** after 15 minutes, requests return `401`. The client calls `/login/refresh`, which revokes the old refresh token and returns a new pair.
4. **Reuse detection:** if an already-revoked refresh token is sent again, it was probably stolen, so every refresh token for that user is revoked.
5. **Logout:** `/logout` revokes the refresh token. The access token still works until it expires (at most 15 minutes).

### Token claims

| Claim | Meaning |
|---|---|
| `sub` | Subject: the user's unique id (as a string), the main answer to "who is this token about?" |
| `username` | Custom claim: the user's name, for display only; it can be stale, so never use it to identify the user. |
| `is_superuser` | Custom claim: whether the user is an admin, so apps can check permissions without calling the login service. |
| `iss` | Issuer: who created the token, so apps can reject tokens that didn't come from this service. |
| `aud` | Audience: who the token is meant for, so an app can reject tokens issued for a different app. |
| `iat` | Issued at: when the token was created, as a Unix timestamp; useful for debugging and revoking old tokens. |
| `exp` | Expiration: when the token stops working; `jwt.decode` checks it automatically, and it's the only way a token ends. |
| `kid` | Key ID (in the header, not the payload): tells apps which public key from the JWKS to verify the signature with. |

## Verifying tokens in another app

Another FastAPI app only needs `uv add "pyjwt[crypto]"` and a dependency like this:

```python
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWKClient

LOGIN_SERVICE = "http://127.0.0.1:8000"

oauth2 = OAuth2PasswordBearer(tokenUrl=f"{LOGIN_SERVICE}/api/v1/login/access-token")
jwks_client = PyJWKClient(f"{LOGIN_SERVICE}/.well-known/jwks.json")  # caches keys


def get_token_user(token: Annotated[str, Depends(oauth2)]) -> dict[str, Any]:
    try:
        key = jwks_client.get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            key.key,
            algorithms=["RS256"],
            audience="my-apps",
            issuer="http://localhost:8000",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

Use `user["sub"]` as the user id, and `user["is_superuser"]` for admin checks.

## Making a user a superuser

There is no API for creating the first admin. Promote a user directly in Postgres (`user` is a reserved word, so it needs quotes):

```sql
UPDATE "user" SET is_superuser = true WHERE username = 'test';
```

The new flag appears in tokens issued after the change.

## Testing

`tests/jwttests.py` is an end-to-end script that tests the **running** server over HTTP. It covers login, JWKS, token claims, rejection of tampered and forged tokens, refresh rotation, reuse detection and logout.

```bash
# terminal 1
uv run fastapi dev app/main.py

# terminal 2
uv run tests/jwttests.py
```

It exits with code `1` if any check fails. Each run creates a new `jwttest_xxxxxxxx` user.

## Key rotation

1. Generate a new key pair and set a new `JWT_KEY_ID`.
2. Publish **both** public keys in JWKS, but sign new tokens with the new private key.
3. Once every token signed with the old key has expired (15 minutes for access tokens), remove the old public key.

## Roadmap

- [ ] React + Vite login frontend (`web/`) with a generated typed API client
- [ ] Docker images for the API and the web app
- [ ] Traefik gateway so every app shares one origin (`/auth`, `/api`, `/notes`, ...)
- [ ] Alembic migrations instead of creating tables on startup
- [ ] `is_active` flag to disable users
- [ ] Create the first superuser from environment variables on startup

from typing import Any

from typing import Any

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from fastapi import APIRouter
from jwt.algorithms import RSAAlgorithm

from app.core import security
from app.core.config import settings

router = APIRouter(tags=["well-known"])

# Build the JWK once at import time; the public key never changes while the app runs
_public_key_obj = load_pem_public_key(security.PUBLIC_KEY.encode())
_jwk = RSAAlgorithm.to_jwk(_public_key_obj, as_dict=True)
_jwk.update({"kid": settings.JWT_KEY_ID, "use": "sig", "alg": security.ALGORITHM})

JWKS = {"keys": [_jwk]}

@router.get("/.well-known/jwks.json")
def jwks() -> dict[str, any]:
    return JWKS
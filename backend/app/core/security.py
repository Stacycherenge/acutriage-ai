# backend/app/core/security.py
import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
ALGORITHM = "RS256"

PRIVATE_KEY = os.getenv("PRIVATE_KEY_STR", "").replace(r"\n", "\n")
PUBLIC_KEY = os.getenv("PUBLIC_KEY_STR", "").replace(r"\n", "\n")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": int(expire.timestamp())})
    
    return jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)

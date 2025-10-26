
# app/security.py
from passlib.context import CryptContext
from app.models.user import User

# Choose argon2id (recommended) and tune costs if needed
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__type="ID",          # Argon2id
    argon2__memory_cost=102400, # ~100 MiB
    argon2__time_cost=2,        # iterations
    argon2__parallelism=8       # lanes/threads
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)



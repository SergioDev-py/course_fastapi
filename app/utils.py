from passlib.context import CryptContext
from .schemas import UserCreate


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash(password: str, hasher: CryptContext = pwd_context):
    hashed_password = hasher.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

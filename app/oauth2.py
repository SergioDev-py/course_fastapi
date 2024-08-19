from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from . import schemas, database, models
import jwt
from jwt import InvalidTokenError
from .config import settings


# tokenurl is the endpoint of the login
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


# We can create a secret key by using this command in the terminal: openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict, expire_delta: int = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data
    
# This function exists because usually here is where you query the user and return it, so we allow endpoints use the user that is being returned
def get_current_user(token: Annotated[str, Depends(oauth2_schema)], db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials :(",
        headers={"WWW-Authenticate": "Bearer"}
    )
    user_info = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == user_info.id).first()

    return user

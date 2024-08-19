from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from ..oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid password")
    
    # Create a return token
    access_token = oauth2.create_access_token(data={"user_id": user.id}, expire_delta=ACCESS_TOKEN_EXPIRE_MINUTES) # data is the content of the payload, don't include sensitive information
    
    return schemas.Token(access_token=access_token, token_type="bearer")

"""
More about OAuth2PasswordRequestForm = https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/?h=oauth2passwordrequestform#oauth2passwordrequestform

OAuth2 specifies that when using the "password flow" (that we are using) the client/user must send a username and password fields as form data.
"""
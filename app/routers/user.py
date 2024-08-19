from fastapi import Depends, status, HTTPException, APIRouter
from .. import models
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserOut, UserCreate
from ..utils import hash
from .. import oauth2


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user.email)
    if user_query.first() is None:
        # Hash the password
        user.password = hash(user.password)

        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The email is already in use, please use a different email")


# Get user
@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if user_query.first():
        return user_query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    user_query.delete(synchronize_session=False)
    db.commit()
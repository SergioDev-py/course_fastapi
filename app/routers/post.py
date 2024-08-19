from fastapi import Depends, status, HTTPException, APIRouter
from .. import models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional
from ..schemas import Post, PostCreate, PostOut


router = APIRouter(
    prefix="/posts", # prefix for all endpoints 
    tags=["Posts"] # gathers all posts endpoint in a group (swagger)
)

# Get all posts
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""): # Always need to pass de db parameter when working with sqlalchemy
    posts = db.query(models.Post, 
                     func.count(models.Vote.post_id).label("Votes")).join(models.Vote, 
                                                                          models.Vote.post_id == models.Post.id, 
                                                                          isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    posts = list(map(lambda x: x._mapping, posts)) # For some reason without this does not work... sqlalchemy
    return posts

"""
# get_posts original function

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Post])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""): # Always need to pass de db parameter when working with sqlalchemy
    sentencia = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip) # SQL query that has not been executed
    posts = sentencia.all() # Execute the query
    return posts
"""


# Get one post
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostOut)
def get_one_post(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first() # filter acts like WHERE (SQL)
    posts = db.query(models.Post, 
                     func.count(models.Vote.post_id).label("Votes")).join(models.Vote, 
                                                                          models.Vote.post_id == models.Post.id, 
                                                                          isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return posts
    


# Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) # **Maps a dictionay of the input into the pydantic object (table)
    # print(f"User id: {current_user.id}, user email: {current_user.email}")
    db.add(new_post) # Add the new post to the stagged
    db.commit() # Commit changes to the DDBB
    db.refresh(new_post) # returns post added
    return new_post


# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id) # Query to find post
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post.delete(synchronize_session=False)
    db.commit()


# Update a post
@router.put("/{id}", response_model=Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post_query.update(post.model_dump(), synchronize_session=False) # ** no needed as in create_post
    db.commit()
    return post_query.first()
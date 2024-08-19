from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Annotated, Optional, Literal


"""
Usually it is good idea to create one model per request
"""

# Format the user info input shoud have
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Format the user info output shold have
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # class Config:
    #     ORM_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


# Format the post input should have
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

# Format the post output should have
class Post(PostBase):
    created_at: datetime
    owner_id: int
    owner: UserOut # We can retrieve a class from another class atribute

    # class Config:
    #     ORM_mode = True


class PostOut(BaseModel):
    Post: Post # the leftmost "Post" needs to be capitalized 
    Votes: int # Votes is capitalized because in post.py, the .label("Votes")) is also capitalized


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)] # Keep in mind this a sugestion from a comment
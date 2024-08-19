from typing import Optional # Optional[int] for example
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import time


load_dotenv()

app = FastAPI()


# Post object to avoid type errors and force a particular input format (Schema)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Database connection
while True:
    try:
        conn = psycopg2.connect(host = os.getenv("HOST"), 
                                database = os.getenv("DATABASE"), 
                                user = os.getenv("USER"), 
                                password = os.getenv("PASSWORD"),
                                cursor_factory = RealDictCursor) # Gives the columns name
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break

    except Exception as error:
        print("Database connection falied!")
        print(f"Error was: {error}")
        time.sleep(3)


@app.get("/")
def root():
    return {"message": "Welcome to my API! :)"}


# Read all posts
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


# Read one post
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def read_one_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,)) # single element tuple "," needed at the end
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found :(")
    else:
        return {"post_details": post}


# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                   (post.title, 
                   post.content, 
                   post.published))
    new_post = cursor.fetchone()
    conn.commit() # Needed to commit changes to DDBB
    return {"data": new_post}


# Delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    if deleted_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found :(")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title,
                                                                                                               post.content,
                                                                                                               post.published,
                                                                                                               id))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found :(")
    conn.commit()
    return {"data": updated_post}

"""
Documentation for psycopg2: https://www.psycopg.org/docs/usage.html
"""
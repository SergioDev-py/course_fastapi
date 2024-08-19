from fastapi import FastAPI
# from . import models
# from .database import engine
from .routers import post, user, auth, votes
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) This can be commentd because alembic is creating the database

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Way to include all endpoints we've created to the app instance
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

# Root
@app.get("/")
def root():
    return {"Message": "Hello World!"}
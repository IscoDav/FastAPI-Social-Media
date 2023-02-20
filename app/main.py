# these libs are used with fast api functions
from fastapi import FastAPI
# to connect with the database
from sqlalchemy.orm import Session
import models  # ORM model tables
from database import engine  # Engine that connects the database with API
from routers import post, users, auth, vote  # routers for fastapi apps
from fastapi.middleware.cors import CORSMiddleware

# Database connections engine
#models.Base.metadata.create_all(bind=engine)


app = FastAPI()  # Calling Fast API requests to the app

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default page test
@app.get('/')
def test_post():
    return {'data': 'OK'}


app.include_router(post.router)  # works with POSTs api routs
app.include_router(users.router)  # works with USERs api routs
app.include_router(auth.router)
app.include_router(vote.router)
# %%

# these libs are used with fast api functions
from fastapi import FastAPI
# to connect with the database
from sqlalchemy.orm import Session
import models  # ORM model tables
from database import engine  # Engine that connects the database with API
from routers import post, users, auth  # routers for fastapi apps

models.Base.metadata.create_all(bind=engine)  # Database connections engine

app = FastAPI()  # Calling Fast API requests to the app


# Default page test
@app.get('/')
def test_post():
    return {'data': 'OK'}


app.include_router(post.router)  # works with POSTs api routs
app.include_router(users.router)  # works with USERs api routs
app.include_router(auth.router)
# %%

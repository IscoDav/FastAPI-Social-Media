import sys
sys.path.append('./app')    # calling local module from another directory
from fastapi import status, Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session  # database connection
import models  # ORM model tables
import schema  # Schemas for POST APIs
import oauth2
from database import get_db  # Database connection

# API router functions to give access main app
router = APIRouter(
    prefix='/posts',  # assigns all routs with this name
    tags=['Posts']    # tag name groups all routs under this name
)
 

# Getting all post info from database
@router.get("/")
def get_post(db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):  # assigning the session with databse
    posts = db.query(models.Post).all()
    return posts


# accepting new data entries and saving it to the database
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db),
                 # Forces user to login before creating any post
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())  # assign each new entry to the database model table

    db.add(new_post)  # adds it into database
    db.commit()  # saving and confirming this action
    db.refresh(new_post)  # refreshing the database
    return new_post  # returning input results to the user


# getting post information with its ID
@router.get("/{id}", response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # filters table with id and gets first appeared results
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # HTTP request is sent if id is not found in database
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')

    return post


# deleting post from database by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating or editing post information by id
@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    posts = post_query.first()

    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

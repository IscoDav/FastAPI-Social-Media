import sys
sys.path.append('..')    # calling local module from another directory
from fastapi import status, Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session  # database connection
import models  # ORM model tables
import schema  # Schemas for POST APIs
import oauth2
from sqlalchemy import func
from database import get_db  # Database connection
from typing import List, Optional

# API router functions to give access main app
router = APIRouter(
    prefix='/posts',  # assigns all routs with this name
    tags=['Posts']    # tag name groups all routs under this name
)
 

# Getting all post info from database
@router.get("/", response_model=List[schema.PostOut])
def get_post(db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user),
             limit: int = 10, skip: int = 0,
             search: Optional[str] = ""):  # assigning the session with databse

    # This function for filtering to get user post only
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # This one returns all post from all users

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


# accepting new data entries and saving it to the database
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db),
                 # Forces user to login before creating any post
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())  # assign each new entry to the database model table

    db.add(new_post)  # adds it into database
    db.commit()  # saving and confirming this action
    db.refresh(new_post)  # refreshing the database
    return new_post  # returning input results to the user


# getting post information with its ID
@router.get("/{id}", response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # filters table with id and gets first appeared results
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # HTTP request is sent if id is not found in database
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')

    return post


# deleting post from database by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # check the user id from database
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')

    # Check the request from user match, in case another user deleting it
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')

    post_query.delete(synchronize_session=False)
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

    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

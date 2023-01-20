import sys

import jwt

sys.path.append('./app')
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  # UserCredentials for password
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from database import get_db
import schema, models, utils, oauth2


router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_credential: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.email == user_credential.username).first()

    # Check the email/user data in database
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    # if there is a such user, we check for password match
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    # create a Token
    # Return Token

    # putting user_id in play load but other data are welcome
    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}



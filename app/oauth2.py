from jose import JWTError, jwt  # for creating JWS token
from datetime import datetime, timedelta
import schema, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config import settings

# login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# ALGORITHM
# Expiration time

# Secret key for creating token to prevent hacking
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes  # minutes


# Encoding the data
def create_access_token(data: dict):
    to_encode = data.copy()  # for manipulation data

    # current time + adding 30 minutes
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # updating dictionary with expire date

    # Creates JWT token with encode_data, our secret key with the algorithm provided
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt  # Returning ready created token


# verify the token whether its valid
def verify_access_token(token: str, credentials_exception):

    try:
        # decodes previous token to check the match
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        # Credential errors if there are some
        if user_id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


# Takes the token from request automatically, extract the id for us which verify the token
# Correctness
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user











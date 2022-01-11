from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm     #Encryption algo to be used
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})       #adding expiry time to the payload

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#called in get_current_user()
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")        #Extracts the id

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)       #Validates the token schema with the one we have provided

    except JWTError:
        raise credentials_exception
    
    return token_data

#Anytime any route needs the user to be loggedin(like create post), we will use this in the function call of that route
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):  #Takes the token from the request, verifies it and fetches the id
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail=f"Could not validate credentials",
                            headers={"WWW-Authentication": "Bearer"})   #add some custom header

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return  user

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm   #To send credentials in form data instead of the body
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    #OAuth2PasswordRequestForm returns a dict with only 2 values, username and password
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials!")

    if not utils.verify(user_credentials.password, user.password):   #Verifies the password
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials!")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})     #data is the payload

    return {"access_token": access_token, "token_type": "bearer"}     #token_type tells user what kind of token is this
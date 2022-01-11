from pydantic import BaseModel, EmailStr  # To define and validate the schema of the data
from datetime import datetime
from typing import Optional
from pydantic.types import conint

#Pydantic model/schema(for validating requests)
#It defines the structure of a request and response
'''
class Post(BaseModel):
    title:      str  # It will try to convert the data into this format
    content:    str
    published:  bool = True  # optional field, defaults to True
    #rating:    Optional[int] = None       #completely optional field, with no default value
'''

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

#Request Schema 
class PostBase(BaseModel):
    title       :  str
    content     :  str
    published   :  bool = True

class PostCreate(PostBase):
    pass

#Response Schema
class Post(PostBase):
    id          : int
    created_at  : datetime
    owner_id    : int
    owner       : UserOut   #Returns a schema of type UserOut

    #Pydantic only knows dicts, it doesn't recognize a sqlalchemy model
    #This class fixes this
    class Config:       
        orm_mode = True  # Tells pydantic to convert the orm to a dict

class PostOut(BaseModel):
    Post: Post
    votes: int

    class config:
        orm_mode = True

class Token(BaseModel):
    access_token   : str
    token_type    : str
    
class TokenData(BaseModel): #for the data embeded in the token
    id: Optional[str] = None

class Vote(BaseModel):
    post_id         : int
    dir             : conint(le=1, ge=0) #Conditional Int. Direction: 1 for vote, 0 for unvote
    

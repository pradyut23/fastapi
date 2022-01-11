from typing import List
from sqlalchemy import func
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from typing import Optional
#from fastapi.params import Body


#To structure the api routes into different modules
router = APIRouter(
    prefix='/posts',
    tags = ['Posts']
)

#get all posts
@router.get('/', response_model=List[schemas.PostOut])
#@router.get('/')
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):        #limit, search and skip are the query parameters (?)
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    #filter(contains) searches if the search  str is present in the title 
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  #.filter(models.Post.owner_id == current_user.id).all() for getting only logged in users post

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    return posts


'''#get latest post
@app.get('/posts/latest')  # route order matters in fastapi. '/posts/latest' below '/posts/{id}' will throw error
def get_latest_post():
    post = my_posts[-1]
    return {'detail': post}'''


#get specific post
@router.get('/{id}', response_model=schemas.PostOut)   # Path parameter is always returned as string
# validation to check id is always int
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    return post


#create new post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
#def create_posts(payload: dict = Body(...)):  #Body() extracts all the data in the body, converts to dict and stores in a variable called payload
# new_post is a Pydantic model which validates data based on the Post model
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):      #get_current_user() asks for login first
    '''cursor.execute(""" INSERT INTO posts (title, content, published)
        VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))  #avoids SQL Injection, which can happen by directly passing {post.title} instead of %s
    new_post = cursor.fetchone()
    conn.commit()'''

    #new_post = models.Post(title=post.title, content=post.content, published=post.published))
    # ** unpacks the dictionary to put into the model
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Equivalent to RETURNING * of psql

    return new_post


#deleting a post
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)  # Just a query
    post = post_query.first()

    if post == None:  # first() runs the query
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post for id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized to perform requested action!")

    post_query.delete(synchronize_session=False)

    db.commit()

    # on deleting no data should be sent back
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#updating post
@router.put("/{id}", response_model=schemas.Post)
# validating the post schema with Post. post received from the frontend
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
                (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()'''

    post_query = db.query(models.Post).filter(models.Post.id == id)
    fetched_post = post_query.first()

    if fetched_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if fetched_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform requested action!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

from sqlalchemy.orm.session import Session
from fastapi import Response, status, HTTPException, APIRouter, Depends
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()  #Checks if the post is present
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with {vote.post_id} not found")
    
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()     #Check if vote exists for that post by that user id

    if(vote.dir == 1):
        if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                    detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)        #Add vote if not found in db
        db.commit()
        return {"message": "successfully added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Vote does not exist")

        vote_query.delete(synchronize_session=False)  #Delete vote if present in the db
        db.commit()
        return {"message": "succesfully deleted vote"}
        
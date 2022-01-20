from hashlib import new
from pstats import Stats
import stat
from statistics import mode
from fastapi import FastAPI, Response, APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    # check if the post to vote exists
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist"
        )

    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id,
        models.Votes.user_id == current_user.id,
    )

    voted = vote_query.first()

    # upvote
    if vote.dir == 1:
        if voted:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {vote.post_id}"
            )
        else:
            new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
            
            db.add(new_vote)
            db.commit()
            
            return {
                "message": "Successfully added vote"
            }
    
    # downvote
    else:
        if not voted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote does not exist"
            )
        else:
            vote_query.delete(synchronize_session=False)
            
            db.commit()

            return {
                "message": "Successfully deleted vote"
            }
    

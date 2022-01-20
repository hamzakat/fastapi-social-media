
from pyexpat import model
from statistics import mode
from typing import List, Optional
from unittest import skip
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']  # tags will improve the categorization in the API docs page
)
# to nest other routers: router.include_router(other.router)

''' Posts routes '''

@router.get("/", response_model=List[schemas.PostVotes])
async def get_posts(db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user),
                limit: int = 10,
                skip: int = 0,
                search: Optional[str] = "") :

    # use this to only read the current user's posts
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    '''
    # Get only posts (w/o votes info):

    query = db.query(models.Post) \
            .filter(models.Post.title.contains(search)) \
            .limit(limit) \
            .offset(skip) \
            .all()
    '''

    '''
    # Get posts w/ votes info

    Corresponding SQL query:
        SELECT posts.*, count(votes.post_id) AS votes 
        FROM posts LEFT OUTER JOIN votes 
        ON posts.id = votes.post_id 
        WHERE (posts.title LIKE '%%' || %(search)s || '%%') GROUP BY posts.id
        LIMIT %(limit)s 
        OFFSET %(skip)s

    '''
    query = db.query(
                models.Post,
                func.count(
                    models.Votes.post_id
                ).label("votes")
            ) \
            .join(
                models.Votes,
                models.Votes.post_id == models.Post.id,
                isouter=True
            ) \
            .group_by(models.Post.id) \
            .filter(models.Post.title.contains(search)) \
            .limit(limit) \
            .offset(skip) \
    
    # print(q)
            
    posts = query.all()

    return posts 



@router.get("/{id}", response_model=schemas.PostVotes)
async def get_post(id: int,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    '''
    # Get post w/o votes info
    query = db.query(models.Post) \
            .filter(models.Post.id  == id) \
            .first()
    '''

    # Get post w/ votes info
    query = db.query(
                models.Post,
                func.count(
                    models.Votes.post_id
                ).label("votes")
            ) \
            .join(
                models.Votes,
                models.Votes.post_id == models.Post.id,
                isouter=True
            ) \
            .group_by(models.Post.id) \
            .filter(models.Post.id  == id)

    post = query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return post



'''
    parameter:
    - status_code determines the code that will be returned in the response when everything run well
    - response_model the schema to use for constructing the response data

'''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)): 
    
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post) # stage changes
    db.commit()  # commit changes
    db.refresh(new_post)    # returning the record

    return new_post



@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(post_id: int,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id  == post_id)
    
    post = post_query.first()

    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} was not found")
    
    #  don't allow not auhtorized users to delete
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit() 

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_posts(id: int,
                post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
                
    post_query = db.query(models.Post).filter(models.Post.id  == id)
    post_to_update = post_query.first()
    
    if not post_to_update: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    #  don't allow not auhtorized users to update
    if post_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
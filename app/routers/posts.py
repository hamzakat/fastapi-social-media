from typing import List
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']  # tags will improve the categorization in the API docs page
)
# to nest other routers: router.include_router(other.router)

''' Posts routes '''

@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()

    return posts

@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id  == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return post

'''
    parameter:
    - status_code determines the code that will be returned in the response when everything run well
    - response_model the schema to use for constructing the response data

'''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    
    new_post = models.Post(**post.dict())
    db.add(new_post) # stage changes
    db.commit()  # commit changes
    db.refresh(new_post)    # returning the record

    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id  == id)
    if not post_query.first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    post_query.delete(synchronize_session=False)
    db.commit() 

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id  == id)
    post_to_update = post_query.first()
    if not post_to_update: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
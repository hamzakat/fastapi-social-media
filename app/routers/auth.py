from os import access
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Auhtentication']
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # check if user is registered
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # check password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # payload data
    # here, we only added user.id, but we can add more public  data
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
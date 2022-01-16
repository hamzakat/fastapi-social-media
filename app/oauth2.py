from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "hey! "
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    encoded = jwt.encode(claims=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        # if payload wasn't decoded successfully, hence, if the id is none, then:
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)   # we can add furhter data fields

    except JWTError as e:
        print(e)
        raise credential_exception
        
    return token_data
    
# this function will be used as a dependency for all operations that require signed in user
def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not vaildate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_access_token(token, credential_exception)
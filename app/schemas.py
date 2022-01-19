'''
    Schema Vaildation:
    - Schemas are used to set data fields to send and receive, while handling request and response data
    - This is used to apply constraints on API 
'''

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# user response (public data that clients receive)
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# "create" and "update" post requests (data that enters the database)
class PostCreate(PostBase):
    # base class fields
    pass

# post response (data that clients receive)
class Post(PostBase):
    # base class fields
    # additional fields
    id: int
    created_at: datetime
    owner_id: int
    owner: User     # pydantic schema/model

    class Config:
        # apply the schema on non-dictionary data (SQLAlchemy query data)
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
'''
    Schema Vaildation:
    - Schemas are used to set data fields to send and receive, while handling request and response data
    - This is used to apply constraints on API 
'''

from datetime import datetime
from pydantic import BaseModel

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

    class Config:
        # apply the schema on non-dictionary data (SQLAlchemy query data)
        orm_mode = True
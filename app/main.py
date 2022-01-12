import time
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2  
from psycopg2.extras import RealDictCursor

posts = [
    {"title": "first post", "content": "anything", "id": 1}
]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# connect to the database
while True:    
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi_social_media', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection was successful")
        break
    except Exception as err:
        print(err)
        time.sleep(2)

def find_post(id):
    for p in posts:
        if p["id"] == id:
            return p
    return None

app = FastAPI()

@app.get("/")
async def root():
    return {"data": "API root"}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()   # use fetchall() to search for and get a set of output 
    return {"data": posts}

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone() # use fetchone() to search for and get one output 

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post}

# status_code parameter determine the code that will be returned in the response when everything run well
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    # it is important to use placeholders %s to prevent SQL injection attacks
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit() # write to the DB and save changes 
    return {"data": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    if not deleted_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_posts(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if not updated_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    conn.commit()
    return {"data": updated_post}
    
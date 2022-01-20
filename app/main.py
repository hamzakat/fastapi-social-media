from fastapi import FastAPI
from . import models 
from .database import engine
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# register routers
app.include_router(posts.router)
app.include_router(users.router, prefix="/users")
app.include_router(users.router, prefix="/u")   # another path for users endpoint
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"data": "API root"}
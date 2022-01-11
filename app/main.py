from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import Engine
from .routers import post, user, auth, vote

#Creates all the models in the database
#models.Base.metadata.create_all(bind=Engine)   #Not needed after alembic

app = FastAPI()

origins = ['*']   #Includes domains that can call this api, like https://www.google.com. Asteriks(*) for a public api which can be called by anyone

app.add_middleware(
    CORSMiddleware,                     #All requests before going through the router first goes through the middleware and performs some functions
    allow_origins=origins,              #What domains are allowed to talk to our api's
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)         #accesses the routes in the post file
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')   #Path operation / Route
async def root():
    return {'message': 'Hello World!!'}


from fastapi import FastAPI, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .routers import user_router, review_router

from .database import User, Movie, UserReview
from .database import database as connection


app = FastAPI(
    title='Proyecto para reseñar películas',
    description='En este proyecto seremos capaces de reseñar películas.',
    version='1'
)

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(review_router)

@api_v1.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):    
    return {
        'username': data.username,
        'password': data.password
    }

app.include_router(api_v1)

@app.on_event('startup')
def starup():
    if connection.is_closed():
        connection.connect()        

        connection.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
      

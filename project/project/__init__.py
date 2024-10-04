from fastapi import FastAPI

from .routers import user_router, review_router

from .database import User, Movie, UserReview
from .database import database as connection


app = FastAPI(
    title='Proyecto para reseñar películas',
    description='En este proyecto seremos capaces de reseñar películas.',
    version='1'
)

app.include_router(user_router)
app.include_router(review_router)

@app.on_event('startup')
def starup():
    if connection.is_closed():
        connection.connect()        

        connection.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
      

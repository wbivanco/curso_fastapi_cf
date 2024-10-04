from fastapi import FastAPI
from fastapi import HTTPException
from typing import List
from database import User, Movie, UserReview
from database import database as connection
from schemas import UserRequestModel, UserResponseModel, ReviewRequestModel, ReviewResponseModel


app = FastAPI(
    title='Proyecto para reseñar películas',
    description='En este proyecto seremos capaces de reseñar películas.',
    version='1'
)

@app.on_event('startup')
def starup():
    if connection.is_closed():
        connection.connect()        

        connection.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        
@app.get('/')
async def index():
    return 'Hola mundo, desde un servidor en FastAPI'

@app.get('/about')
async def about():
    return 'About'

@app.post('/users', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El usuario ya existe.')

    hash_password = User.create_password(user.password)

    user = User.create(
        username=user.username, 
        password=hash_password
    )

    return UserResponseModel(id=user.id, username=user.username)


@app.post('/reviews', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):

    if User.select().where(User.id == user_review.user_id).exists():
        raise HTTPException(404, 'El usuario no existe.')
    
    if Movie.select().where(Movie.id == user_review.movie_id).exists():
        raise HTTPException(404, 'La película no existe.')
    
    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score 
    )

    return user_review

@app.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews():
    reviews = UserReview.select()

    return [user_review for user_review in reviews]


@app.get('/reviews/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(404, 'La reseña no existe.')

    return user_review
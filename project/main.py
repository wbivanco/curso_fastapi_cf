from fastapi import FastAPI
from fastapi import HTTPException
from database import User, Movie, UserReview
from database import database as connection
from schemas import UserBaseModel


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

@app.post('/users')
async def create_user(user: UserBaseModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El usuario ya existe.')

    hash_password = User.create_password(user.password)

    user = User.create(
        username=user.username, 
        password=hash_password
    )

    return user.id
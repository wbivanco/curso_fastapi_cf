from fastapi import HTTPException, APIRouter, Response, Cookie, Depends
from fastapi.security import HTTPBasicCredentials

from typing import List

from ..database import User
from ..common import get_current_user
from ..schemas import UserRequestModel, UserResponseModel, ReviewResponseModel


router = APIRouter(prefix='/users')

@router.post('', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El usuario ya existe.')

    hash_password = User.create_password(user.password)

    user = User.create(
        username=user.username, 
        password=hash_password
    )

    return UserResponseModel(id=user.id, username=user.username)


@router.post('/login', response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):

    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(404, 'El usuario no existe.')

    if user.password != User.create_password(credentials.password): 
        raise HTTPException(401, 'La contraseña es incorrecta.')

    response.set_cookie(key='user_id', value=user.id)
    return user


@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user: User = Depends(get_current_user)):
    
    return [user_review for user_review in user.reviews]


"""
@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user_id: int = Cookie(None)):

    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(404, 'El usuario no existe.')

    return [user_review for user_review in user.reviews]
"""
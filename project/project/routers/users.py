from fastapi import HTTPException, APIRouter
from fastapi.security import HTTPBasicCredentials


from ..database import User
from ..schemas import UserRequestModel, UserResponseModel


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
async def login(credentials: HTTPBasicCredentials):

    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(404, 'El usuario no existe.')

    if user.password != User.create_password(credentials.password): 
        raise HTTPException(401, 'La contraseña es incorrecta.')

    return user
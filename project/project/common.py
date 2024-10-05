import jwt

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from .database import User


SECRET_KEY = 'secretooculto'
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth")


def create_access_token(user, days=7):
    data = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=days)
    }

    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception as err:
        return None


def get_current_user(token: str = Depends(oauth2_schema)):
    data = decode_access_token(token)

    if data:
        return User.select().where(User.id == data.get('user_id')).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token inválido',
            headers={'WWW-Authenticate': 'Bearer'}
        )
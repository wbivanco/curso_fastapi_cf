from pydantic import BaseModel
from pydantic import validator


class UserBaseModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, usarname):
        if len(usarname) < 3 and len(usarname) > 50:
            raise ValueError('La longitud debe estar entre 3 y 50 caracteres.')
        
        return usarname
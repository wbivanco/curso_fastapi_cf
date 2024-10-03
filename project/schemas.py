from pydantic import BaseModel, validator
from pydantic.utils import GetterDict

from typing import Any

from peewee import ModelSelect


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        
        return res
    

class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, usarname):
        if len(usarname) < 3 and len(usarname) > 50:
            raise ValueError('La longitud debe estar entre 3 y 50 caracteres.')
        
        return usarname
    

class UserResponseModel(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
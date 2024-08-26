from pydantic import BaseModel,EmailStr
from enum import Enum

class UserSchema(BaseModel):
    email:EmailStr
    username:str
    password:str


class Roles(Enum):
    user = "user"
    admin = "admin"
    #is_active:bool=False 
    #role:Roles = "user"

    class Config:
        orm_mode = True
from fastapi import APIRouter,Depends,Form,HTTPException
from sqlalchemy.orm import Session
from database.connection import sess_db


#Repository
from repository.user import UserRepository

#Model
from models.user import UserModel

router = APIRouter()


@router.post("/signup")
def signup_user(db:Session=Depends(sess_db),username : str = Form(),email:str=Form(),password:str=Form()):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    if db_user:
        return "username is not valid"
    
    signup = UserModel(email = email,username = username,password = password)
    success = userRepository.create_user(signup)
    if success:
        return "create user successfully"
    else:
        raise HTTPException(
            status_code=401,detail = "Credentials not correct"
        )
    

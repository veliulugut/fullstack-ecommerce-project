from fastapi import APIRouter,Depends,Form,HTTPException,Response
from sqlalchemy.orm import Session
from database.connection import sess_db
from security.secur import get_password_hash,verify_password,create_access_token,verify_token
from starlette.responses import RedirectResponse

#Repository
from repository.user import UserRepository

#Model
from models.user import UserModel

#security
from security.secur import COOKIE_NAME

router = APIRouter()


@router.post("/signup")
def signup_user(db:Session=Depends(sess_db),username : str = Form(),email:str=Form(),password:str=Form()):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    if db_user:
        return "username is not valid"
    
    signup = UserModel(email = email,username = username,password = get_password_hash(password))
    success = userRepository.create_user(signup)
    if success:
        return "create user successfully"
    else:
        raise HTTPException(
            status_code=401,detail = "Credentials not correct"
        )
    


@router.post("/signin")
def sigin_user(response:Response,db:Session=Depends(sess_db),username : str = Form(),password:str=Form()):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    if not db_user:
        return "username or password is not valid"
    
    if verify_password(password,db_user.password):
        token = create_access_token(db_user)
        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            httponly=True,
            expires=1800
        )
        return {COOKIE_NAME:token,"token_type":"bearer"}
    

@router.get('/verify/{token}')
def verify_user(token,db:Session=Depends(sess_db)):
    userRepository = UserRepository(db)
    payload = verify_token(token)
    username = payload.get("sub")
    db_user = userRepository.get_user_by_username(username)

    if not username:
        raise HTTPException(
            status_code=401,detail="Invalid token"
        )
    
    if db_user.is_active == True:
        return " your account has been allready activated"
    db_user.is_active=True
    db.commit()
    response = RedirectResponse(url="/user/signin")
    return response


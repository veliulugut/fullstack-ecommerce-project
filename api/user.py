from fastapi import APIRouter,Depends,Form,HTTPException,Request,Response
from sqlalchemy.orm import Session
from database.connection import sess_db
from security.secur import get_password_hash,verify_password,create_access_token,verify_token
from starlette.responses import RedirectResponse
import os
from fastapi_mail import  MessageSchema

#Repository
from repository.user import UserRepository

#Model
from models.user import UserModel

#security
from security.secur import COOKIE_NAME

#Mail
from utils.email import fm

FRONTEND_URL = os.getenv("FRONTEND_URL")

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
        return {COOKIE_NAME:token}
    

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

@router.post('/password-reset')
async def password_reset(db:Session=Depends(sess_db),email:str=Form()):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_email(email)

    if not db_user:
        raise HTTPException(status_code=404,detail="User not found")
    
    token = create_access_token(db_user)
    reset_link=f"{FRONTEND_URL}/reset-password?token={token}"

    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[db_user.email],
        body=f"Click on the link to reset your password: {reset_link}",
        subtype="html"
    )

    await fm.send_message(message)
    
    return {"message": "Password reset email sent"}

@router.post('/reset-password')
def reset_password(token: str = Form(), new_password: str = Form(), db: Session = Depends(sess_db)):
    try:
        payload = verify_token(token)
        userRepository = UserRepository(db)
        db_user = userRepository.get_user_by_username(payload.get("sub"))
        
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db_user.password = get_password_hash(new_password)
        db.commit()
        
        return {"message": "Password reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    
    
@router.put('/update-profile')
def update_profile(
    db: Session = Depends(sess_db),
    username: str = Form(),
    email: str = Form(),
    new_password: str = Form(),
):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.email = email
    if new_password:
        db_user.password = get_password_hash(new_password)
    
    db.commit()

    return{"message":"profile updated successfully"}

@router.get('/profile')
def get_profile(
    request: Request,
    db: Session = Depends(sess_db),
):
    userRepository = UserRepository(db)
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="unauthorized access")

    try:
        payload = verify_token(token)
        username = payload.get("sub")
        db_user = userRepository.get_user_by_username(username)

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"username": db_user.username, "email": db_user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid token")
    
@router.post('/logout')
def logout(response: Response):
    response.delete_cookie(key=COOKIE_NAME)
    return {"message": "Logged out successfully"}
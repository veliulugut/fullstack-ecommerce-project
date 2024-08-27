import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from fastapi import HTTPException


load_dotenv()

JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="user/signin")
COOKIE_NAME="Authorization"

#create token
def create_access_token(user):
    try:
        payload={
            "username":user.username,
            "email":user.email,
            "role":user.role.value,
            "active":user.is_active,
        }
        return jwt.encode(payload,key=JWT_SECRET_KEY,algorithm=ALGORITHM)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    

#create verify token
def verify_token(token):
    try:
        payload=jwt.decode(token,key=JWT_SECRET_KEY)
        return payload
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

#password hashing
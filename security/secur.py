import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
import logging
import sys
from datetime import datetime, timedelta
import jwt 
from fastapi import Depends,Request
from models.user import UserModel

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#Save to token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/signin")
COOKIE_NAME = "Authorization"

def create_access_token(user):
    try:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": user.username,
            "email": user.email,
            "role": user.role.value,
            "active": user.is_active,
            "exp": expire,
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
        logging.info(f"Token created: {token}")
        return token
    except Exception as e:
        logging.error(f"Token creation failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token creation failed")

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        logging.info(f"Token content: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        logging.error("Token expired")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        logging.error("Invalid token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Geçersiz token")
    except Exception as e:
        logging.error(f"Token validation failure: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token validation failure")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user_from_token(token:str=Depends(oauth2_scheme)):
    user=verify_token(token)
    return user

def get_current_user_from_cookie(request:Request)-> UserModel:
    token=request.cookies.get(COOKIE_NAME)
    if token:
        user = verify_token(token)
        return user
    
from sqlalchemy import Column, Integer, String,Boolean,Enum,DateTime,func
from schema.user import Roles
from datetime import datetime

from database.connection import Base

class UserModel(Base):
    __tablename__ = "users"
    id=Column(Integer, primary_key=True,index=True)
    email = Column(String,unique=True,index=True)
    username = Column(String,unique=True,index=True)
    password = Column(String,unique=False,index=True)
    is_active = Column(Boolean,default=False)
    role = Column(Enum(Roles),default="user")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime,default=func.now(),onupdate=func.now())

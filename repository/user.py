from sqlalchemy.orm import Session
from models.user import UserModel
from typing import Dict,Any

class UserRepository:
    def __init__(self,sess:Session):
        self.sess: Session = sess

    
    def create_user(self,signup:UserModel) -> bool:
        try:
             self.sess.add(signup)
             self.sess.commit()
        except:
            self.sess.rollback()
            return False
        
        return True
    

    def get_user(self):
        return self.sess.query(UserModel).all()
    
    def get_user_by_id(self,id:int):
        return self.sess.query(UserModel).filter(UserModel.id == id).first()
    
    def get_user_by_username(self,username:str):
        return self.sess.query(UserModel).filter(UserModel.username == username).first()
    
    def get_user_by_email(self,email:str):
        return self.sess.query(UserModel).filter(UserModel.email == email).first()
    
    def update_user(self,id:int,details:Dict[str,Any])-> bool:
        try:
            self.sess.query(UserModel).filter(UserModel.id == id).update(details)
            self.sess.commit()
            
        except:
            self.sess.rollback()
            return False
        
        return True
    
    def delete_user(self,id:int)-> bool:
        try:
            self.sess.query(UserModel).filter(UserModel.id == id).delete()
            self.sess.commit()
        except:
            self.sess.rollback()
            return False
        
        return True


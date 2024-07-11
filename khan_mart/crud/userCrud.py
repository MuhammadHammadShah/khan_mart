from  fastapi import HTTPException , status , Depends
from khan_mart.Models.UserModel import UserCreate,User
# from app.api.deps import GET_SESSION
from sqlmodel import Session , select 
from khan_mart.core.logging import logConfig
from sqlalchemy.exc import IntegrityError
from khan_mart.core.security import get_hashed_password,create_Access_Token,Refresh_Token
from datetime import datetime , timedelta , timezone
from khan_mart.core.settings import settings

logger=logConfig(__name__)

class ForUser():
  
    def _Chk_User_Exist(*,self,username:str|None=None,email:str|None=None,session:Session):
     
     if username  and not email:
        user:User|None=session.exec(select(User).where(User.name==username)).one_or_none();
    #   if  user :
        #   raise HTTPException(status_code=status.HTTP_302_FOUND,detail="User  found  please change your username")
    #   return False
        return user
    
     elif  email and not username  :
        user:User|None=session.exec(select(User).where(User.email==email)).one_or_none;
        return user
  
  
    def Registration(*,self,usercrate:UserCreate , session:Session):
      
      try:
        
          if isinstance(self._Chk_User_Exist(username=usercrate.name , session=session),User):
              raise HTTPException(status_code=status.HTTP_302_FOUND,detail="User  found  please change your Username")
            
          if  isinstance(self._Chk_User_Exist(email=usercrate.email,session=session)):
              raise HTTPException(status_code=status.HTTP_302_FOUND,detail="User  found  please change Your Eamil ")
          
          R_User=User.model_validate(
              usercrate, update={"hashed_Password":get_hashed_password(usercrate.password)}
              )
    
          session.add(R_User)
          session.commit()
          
        #   Get the User from DB
          
          Real_User:User=session.refresh(R_User)

          #  Create Access Token          
          expireTime=timedelta(days=settings.TOKEN_ACCESS_EXPIRTES_TIMES)
          return create_Access_Token(data={"id":1,"username":"zayn"},expires=timedelta(days=expireTime))
        
      except HTTPException as e:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{e}") from  e 
      except Exception as e :
          logger.error(f"{e}")
          raise HTTPException(
              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail="unexpected Occur Thrown by server"
          )   from e

    def Login(*,self):
        ...
          
           
    

boy=ForUser();    
    

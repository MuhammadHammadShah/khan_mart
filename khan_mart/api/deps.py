from fastapi import HTTPException , status , Depends
import jwt
from jwt.exceptions import InvalidTokenError

from sqlmodel import SQLModel ,Field , Session ,select
from  khan_mart.core.db_settings import engine
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated , Union
from khan_mart.core.settings import settings
from khan_mart.Models.UserModel import User , Payload



auth_schema=OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access_token")


def  get_db_session():
    with Session(engine) as session:
        yield session

        
GET_SESSION=Annotated[Session,Depends(get_db_session)]

Token_DEP=Annotated[str,Depends(auth_schema)]

def getCurrentUser(token:Token_DEP  ,session:GET_SESSION):
    ...        
    # Get Payload 
    try:     
        paylod=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        
        tokenData=Payload(**paylod)
        
        id:int=tokenData.get("id",None)
        username:str=tokenData.get("username",None)
        
        if not username :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token"
                )
        
        # if not id:
            
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Invalid Token",
        #         headers={"WWW-Authenticate":"Bearer"}
        #         )
            
        if id :
            
            user:User=session.get(User,id)
            
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Token",
                    headers={"WWW-Authenticate":"Bearer"}
                )
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Inactive User"               
                    )
            
            return user
        else :
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token",
                headers={"WWW-Authenticate":"Bearer"}
            )
    
    except InvalidTokenError :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Credentials ",
            headers={"WWW-Authenticate":"Bearer"}
        )    
    
    
Current_User=Annotated[User,Depends(getCurrentUser)]


def get_Current_Active_SuperUser(superUser:Current_User):
    ...
    if not superUser.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have enogh priviliges",
            headers={"WWW-Authenticate":"Bearer"}
            )
    return superUser


GET_CURR_ACT_SUPER_USER=Annotated[User,Depends(get_Current_Active_SuperUser)] 


def verify_SuperUser(session:GET_SESSION,userId:int):
    ...
    user:User=session.get(User,userId)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="Inactive User"   
        )
    
    
    if not user.is_verified:
         raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="Inactive User"   
        )
         
    return user


VERIFY_SUP_USER_BY_ID=Annotated[User,Depends(verify_SuperUser)]  


import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime ,timedelta , timezone
from typing import Annotated , Union
from fastapi import HTTPException , status
from khan_mart.core.settings import settings

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


def verify_Password(password:str,hashed_password:str):
    ...
    return pwd_context.verify(password,hashed_password)

def get_hashed_password(password:str):
    return pwd_context.hash(password)

def create_Access_Token(*,data:dict[str,Union[str,int]],expires:Union[timedelta|None]=None):
    to_encode=data.copy()
    if expires:
        expire= datetime.now(timezone.utc) + expires
        expires_in_str = expire.strftime('%Y-%m-%dT%H:%M:%SZ')
        # expire= datetime.utcnow() + expires
    else :
        expire= datetime.now(timezone.utc) + timedelta(days=1)
        expires_in_str = expire.strftime('%Y-%m-%dT%H:%M:%SZ')
    to_encode.update({"exp_is":expires_in_str})
    return  jwt.encode(to_encode , settings.SECRET_KEY , settings.ALGORITHM )

    
# def Token_Decoder(token:str):
#     ...        

def Refresh_Token(*,data:dict[str,Union[str,int]],expires:Union[timedelta,None]=None):

    ...
    to_encode = data.copy()

    if expires:
        expire_is= datetime.now(timezone.utc) + expires
    else :
        expire_is=datetime.utcnow() + expires
    
    to_encode.update({"exp_is":expire_is})
    
    return jwt.encode(to_encode,settings.SECRET_KEY,settings.ALGORITHM) 

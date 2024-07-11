from sqlmodel import SQLModel , Field
from typing import Annotated , Union 
from khan_mart.Models.BaseClass import BaseID
from khan_mart.Models.Roles import Roles

class UserBase(SQLModel):
    name:Annotated[str,Field(min_length=3)]
    email:Annotated[str,Field(min_length=8 , max_length=20)]
    age:Annotated[int,Field(ge=10)]
    is_active:bool=True
    is_verified:bool=Field(default=False)
    # Role:Annotated[Roles,Field(default=Roles.normalUser)]



class UserCreate(UserBase):
    password:str=Field(min_length=3)  
    
    
class User(BaseID,UserBase,table=True):
    hashed_Password:str=Field(min_items=3)
      
    
class UserUpdate(SQLModel):
    ...
    email:str|None=None
    name:str|None=Field(default=None) 
    
    
class  ResetPass(SQLModel):
    # password:str
    ...       
    
class ForgetPass(SQLModel):
    
    ...
    
    
class UpdatePassword(SQLModel):
    current_password: str
    new_password: str  
    

class Payload(SQLModel):

    sub:dict[str,Union[str,int]] | None = None


class Token(SQLModel):
    access_token:str
    refresh_token:str
    token_type:str="bearer"
    
class NewPassword(SQLModel):
    token:str
    new_Password:str    
            
from fastapi import FastAPI ,APIRouter,HTTPException,status
from khan_mart.Models.UserModel  import UserCreate  
from sqlmodel import SQLModel ,Session
from khan_mart.api.deps import GET_SESSION
from khan_mart.core.logging import logConfig
from khan_mart.crud.userCrud import boy


router = APIRouter()

logger=logConfig(__name__)


@router.get("/getUser")
def getUser():
    ...
    

# def UsersRegistration(User:UserCreate,session:GET_SESSION):
@router.post("/regiter")
def UsersRegistration(user:UserCreate,session:GET_SESSION):
    try:

        logger.info("User Creation Executing ")
        
        
        # code for Registration 
        return boy.Registration(usercrate=user,session=session)
        ...
        
        
    
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )    
    
    except  Exception as e:
        logger.error(e)   
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        )  
        
    
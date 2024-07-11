from pydantic_settings import BaseSettings , SettingsConfigDict 

from typing_extensions import Self

import secrets

import warnings

from typing import Annotated,Literal
from khan_mart.core.utils import parse_cors
from pydantic import (
    BeforeValidator,
    model_validator,
    computed_field,
    AnyUrl
)

class Setting(BaseSettings):
    
    model_config=SettingsConfigDict(
        env_file=".env" , env_ignore_empty=True, extra="ignore"
    )
    
    
    PROJECT_NAME:str
    
    DATABASE_URL:str
    
    ENVIRNMENT:Literal["local","production"]="local"
    
    SECRET_KEY:str=secrets.token_urlsafe(32)
    
    API_V1_STR:str="api/v1"
    
    TOKEN_ACCESS_EXPIRTES_TIMES:int = 1  #  1 day
    REFRESH_TOEKN_EXPIRES_TIMES:int = 7  #  7 days
    
    ALGORITHM:str
    
    DOMAIN:str="localhost:3000"  
    
    BACKENED_CORS:Annotated[list[AnyUrl]|str,BeforeValidator(parse_cors)]=[]
    
    
    @computed_field
    @property
    def server_host(self)->str:
        return f"{self.DOMAIN}" if self.ENVIRNMENT=="local" else  f"https://{self.DOMAIN}"
    
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    
    EMAILS_FROM_EMAIL:str | None=None
    EMAIL_FROM_NAME:str | None=None
    
    
    
    @model_validator(mode="after")
    def _setDefaultEmialsFrom(self)->Self:
        if self.EMAIL_FROM_NAME is None:
            warnings.warn(
                "Emails From name nit set yet , Using Emials from Email instead"
            )
            self.EMAIL_FROM_NAME=self.PROJECT_NAME
        return self 
    

   


    @computed_field
    @property
    def Email_Enabled(self)->bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)  
   
   
    def _check_Default_SecKeys(*,self,Variable_Name:str,Variable_Value:str):
        if Variable_Value=="oyehoyebadobadi":
            message=(
                f"{Variable_Name } :: Default  Value : ->  {Variable_Value} is not secure Secret Key , please change it to a secure value , at least for Deployment"
            )
            if self.ENVIRNMENT=="local":
                warnings.warn(message)
            
            else: 
                raise ValueError(message)
        
    def _check_Default_Password_Mail(*,self,Variable_Name:str,Variable_Value:str):
        if Variable_Value=="Zendaya@actor@hollywood":
            message=(
                f"{Variable_Name}  ::  Default value ::{Variable_Value} is not secure , please change it to a secure Password , at least for Deployment"
            )
            if self.ENVIRNMENT=="local":
                warnings.warn(message)
            
            else: 
                raise ValueError(message)
    
    
    model_validator(mode="after")
    def _enforceNonDefaultSecrets(self)->Self:
        ... 
        self._check_Default_SecKeys(Variable_Name="Secret Key",Variable_Value=self.SECRET_KEY)   
        self._check_Default_SecKeys(Variable_Name="SMTP Password",Variable_Value=self.SMTP_PASSWORD)   
        return self    
        
settings=Setting()




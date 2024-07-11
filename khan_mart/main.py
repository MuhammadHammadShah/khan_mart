from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.responses import RedirectResponse
from khan_mart.core.settings import settings
from khan_mart.core.logging import logConfig
from khan_mart.core.db_settings import engine 
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from khan_mart.api.v1.connect import connect 

logger = logConfig(__name__)

@asynccontextmanager
def lifespan(app:FastAPI):
   ...
   
   logger.info("Server has been Started")
    
   yield 
   
   logger.info("Server has stoped")
   
   
app:FastAPI=FastAPI()

if settings.BACKENED_CORS:
   app.add_middleware(
      CORSMiddleware,
      allow_origins=[str(origin).strip("/") for origin in settings.BACKENED_CORS],
       allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
   )

app.include_router(connect,prefix=f"/{settings.API_V1_STR}",)



@app.get("/")
def root():
    return  RedirectResponse(url="/docs") 
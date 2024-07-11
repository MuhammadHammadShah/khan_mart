from fastapi import APIRouter
from khan_mart.api.v1.Routes import user
connect=APIRouter()

connect.include_router(user.router, prefix="/user",tags=["Users"] )
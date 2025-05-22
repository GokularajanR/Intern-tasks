from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from controllers.user_models import create_user, login_user

class User(BaseModel):
    username: str
    password: str
    role: str

user_route = APIRouter()

@user_route.post("/signup/")
async def signup(request: User):
    try:
        if not request.username or not request.password or not request.role:
            return JSONResponse(status_code=400, content={"message": "All fields are required"})
        if request.role not in ["admin", "user"]:
            return JSONResponse(status_code=400, content={"message": "Invalid role"})
        result = await create_user(username=request.username, password=request.password, role=request.role)
        if not result:
            return JSONResponse(status_code=500, content={"message": "Error creating user"})
        return JSONResponse(status_code=200, content={"message": "User created successfully", "user_id": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    
@user_route.post("/login/")
async def login(request: User):
    try:
        result = await login_user(username=request.username, password=request.password)
        if not result:
            return JSONResponse(status_code=500, content={"message": "Error logging in"})
        return JSONResponse(status_code=200, content={"message": "Login successful", "token": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
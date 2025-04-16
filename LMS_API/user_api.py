import uvicorn
from fastapi import HTTPException, Path, Query, status, APIRouter
from pydantic import BaseModel

from lib_package import User_catalog

router = APIRouter()
users = User_catalog()

class User_Input(BaseModel):
    name: str 
    uid: str 
    ph_no: str

class User_Output(BaseModel):
    name: str
    uid: str
    ph_no: str

@router.post("/users")
async def add_user_api(user_data: User_Input):
    users.add_user(name=user_data.name, uid=user_data.uid, ph_no=user_data.ph_no)
    return User_Output(**user_data.dict())

@router.delete("/users/{uid}")
async def remove_user_api(uid: str = Path(...)):
    success = users.remove_user(uid)
    if success:
        return {"message": "user removed."}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found."
        )

@router.get("/users")
async def get_users_api():
    return users.get_all_users()


@router.get("/users/{uid}")
async def get_user_api(uid: str = Path(...)):
    user = users.get_user_by_uid(uid)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
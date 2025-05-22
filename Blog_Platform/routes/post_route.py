from fastapi import APIRouter, Query
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from controllers.post_models import create_post, get_all_posts, get_post_by_id, update_post, delete_post
from controllers.user_models import verify_jwt_token

class Post(BaseModel):
    title: str
    content: str
    created_by: str
    token: str

post_route = APIRouter()

@post_route.post("/posts/")
async def add_post(request: Post):
    try:
        payload = verify_jwt_token(request.token) # User id, username, role and expiration
        if not payload:
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        if payload["username"] != request.created_by:
            return JSONResponse(status_code=403, content={"message": "Forbidden"})
        if payload["role"] != "admin":
            return JSONResponse(status_code=403, content={"message": "Forbidden"})
        result = await create_post(title=request.title, content=request.content, username=request.created_by)
        if not result:
            return JSONResponse(status_code=500, content={"message": "Error creating post"})
        return JSONResponse(status_code=200, content={"message": "Post created successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error creating post : " + str(e)})
    
@post_route.get("/posts/")
async def get_posts(token: str = Query(...)):
    try:
        payload = verify_jwt_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"message" : "Unauthorised"})
        result = await get_all_posts()
        if not result:
            return JSONResponse(status_code=500, content={"message" : "Error fetching posts"})
        return JSONResponse(status_code=200, content={"Posts" : result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message" : "Error fetching posts : " + str(e)})
    
@post_route.get("/posts/{id}")
async def get_post(id: int, token: str = Query(...)):
    try:
        payload = verify_jwt_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"message" : "Unauthorised"})
        result = await get_post_by_id(id)
        if not result:
            return JSONResponse(status_code=500, content={"message" : "Error fetching posts"})
        return JSONResponse(status_code=200, content={"Posts" : result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message" : "Error fetching posts : " + str(e)})
    
@post_route.delete("/posts/{id}")
async def del_post(id: int, token: str = Query(...)):
    try:
        payload = verify_jwt_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"message" : "Unauthorised"})
        if payload["role"] != "admin":
            return JSONResponse(status_code=403, content={"message" : "Forbidden"})
        result = await delete_post(id)
        if not result:
            return JSONResponse(status_code=500, content={"message" : "Error deleting posts"})
        return JSONResponse(status_code=200, content={"message" : "Post deleted successfully"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message" : "Error deleting posts : " + str(e)})
    
@post_route.put("/posts/{id}")
async def updt_post(id: int, request: Post, token: str = Query(...)):
    try:
        payload = verify_jwt_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"message" : "Unauthorised"})
        if payload["role"] != "admin":
            return JSONResponse(status_code=403, content={"message" : "Forbidden"})
        result = await update_post(id, title=request.title, content=request.content)
        if not result:
            return JSONResponse(status_code=500, content={"message" : "Error updating posts"})
        return JSONResponse(status_code=200, content={"message" : "Post updated successfully"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message" : "Error updating posts : " + str(e)})
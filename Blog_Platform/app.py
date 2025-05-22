import uvicorn
from fastapi import FastAPI

from routes.user_route import user_route
from routes.post_route import post_route

app = FastAPI()
app.include_router(user_route)
app.include_router(post_route)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
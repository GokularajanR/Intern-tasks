from fastapi import FastAPI
from controllers.student_route import std_router

app = FastAPI()
app.include_router(std_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
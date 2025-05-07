import uvicorn
from fastapi import FastAPI
from controllers.book_route import book_route
from controllers.author_route import author_route

main_api = FastAPI()
main_api.include_router(book_route)
main_api.include_router(author_route)

if __name__ == "__main__":
    uvicorn.run("app:main_api", host="127.0.0.1", port=8000, reload=True)
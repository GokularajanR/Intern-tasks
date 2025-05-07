from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from models.author_models import add_author_db, get_all_authors_db, get_author_data_db, get_author_books_db

class Author(BaseModel):   
    name: str
    email: str


author_route = APIRouter()

@author_route.post("/authors/")
async def add_author(request: Author):
    result = await add_author_db(name=request.name, email=request.email)
    if not result:
        return JSONResponse(status_code=500, content={"message": "Error adding author"})
    return JSONResponse(status_code=200, content={"message": "Author added successfully", "author_id": result})

@author_route.get("/authors/")
async def get_all_authors():
    authors = await get_all_authors_db()
    if not authors:
        return JSONResponse(status_code=404, content={"message": "No authors found"})
    return JSONResponse(status_code=200, content={"authors": authors})

@author_route.get("/authors/{author_id}/")
async def get_author_data(author_id: int):
    author_data = await get_author_data_db(author_id)
    if not author_data:
        return JSONResponse(status_code=404, content={"message": "Author not found"})
    return JSONResponse(status_code=200, content={"author": author_data})

@author_route.get("/authors/{author_id}/books/")
async def get_author_books(author_id: int):
    books = await get_author_books_db(author_id)
    if not books:
        return JSONResponse(status_code=404, content={"message": "No books found for this author"})
    return JSONResponse(status_code=200, content={"books": books})
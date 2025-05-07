from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from models.book_models import add_book_db, get_all_books_db, get_book_data_db, get_all_books_db_p

class Book(BaseModel):
    title: str
    genre: str
    author_id: int

book_route = APIRouter()

@book_route.post("/books/")
async def add_book(request: Book):
    result = await add_book_db(title=request.title, genre=request.genre, author_id=request.author_id)
    if not result:
        return JSONResponse(status_code=500, content={"message": "Error adding book"})
    return JSONResponse(status_code=200, content={"message": "Book added successfully", "book_id": result})

@book_route.get("/books/")
async def get_all_books():
    books = await get_all_books_db()
    if not books:
        return JSONResponse(status_code=404, content={"message": "No books found"})
    return JSONResponse(status_code=200, content={"books": books})

@book_route.get("/books/{book_id}/")
async def get_book_data(book_id: int):
    book_data = await get_book_data_db(book_id)
    if not book_data:
        return JSONResponse(status_code=404, content={"message": "Book not found"})
    return JSONResponse(status_code=200, content={"book": book_data})

@book_route.get("/books/paginated/xyz")
async def get_all_books_p(page: int = 1, page_size: int = 5):
    books = await get_all_books_db_p(page=page, page_size=page_size)
    if not books:
        return JSONResponse(status_code=404, content={"message": "No books found"})
    return JSONResponse(status_code=200, content={"page": page, "page_size": page_size, "books": books})
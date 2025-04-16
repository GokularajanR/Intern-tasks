import uvicorn
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel

from lib_package import catalog
from user_api import router

#validation classes
class Book_schema(BaseModel): 
    title: str 
    author: str 
    isbn: str

class msgr(BaseModel):
    message: str

app = FastAPI()
cat = catalog()
app.include_router(router)


@app.post("/books")
async def add_book_api(book_data: Book_schema):
    success = cat.add_book(title=book_data.title, author=book_data.author, isbn=book_data.isbn)

    if success:
        return book_data
    else:
        current_books = cat.load_json()
        if current_books is not False and any(b.get('isbn') == book_data.isbn for b in current_books):
             raise HTTPException(
                 status_code=status.HTTP_409_CONFLICT,
                 detail=f"Book with ISBN '{book_data.isbn}' already exists."
             )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="book add failed."
            )


@app.delete("/books/{isbn}")
async def remove_book_api(isbn: str = Path(...)):
    success = cat.remove_book(isbn)
    if success:
        return {"message": f"Book with ISBN '{isbn}' removed successfully."}
    else:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN '{isbn}' not found or failed to remove."
        )

@app.get("/books",)
async def get_books_api():
    books = cat.load_json()
    if books is False: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load book catalog from file."
        )
    return books


@app.get("/books/search")
async def search_books_api(key: str = Query(...)):
    if not key:
         return []
    results = cat.search_book(key)
    if results is False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during the book search."
        )
    return results if isinstance(results, list) else []


@app.get("/books/{isbn}")
async def get_book_api(isbn: str = Path(...)):
    books = cat.load_json()
    if books is False:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load book catalog from file."
        )

    res = next((book for book in books if book.get("isbn") == isbn), None)

    if res:
        return res
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN '{isbn}' not found."
        )


if __name__ == "__main__":
     uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
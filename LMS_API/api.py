# api.py
import uvicorn
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel

from lib_package import User, User_cat, catalog

#validation classes
class User_Input(BaseModel):
    name: str 
    uid: str 
    ph_no: str

class User_Output(BaseModel):
    name: str
    uid: str
    ph_no: str

class Book_schema(BaseModel): 
    title: str 
    author: str 
    isbn: str

class msgr(BaseModel):
    message: str

app = FastAPI()
cat = catalog()
users = User_cat()

#endpoints
@app.post("/users")
async def add_user_api(user_data: User_Input):
    if users.get_user_by_uid(user_data.uid):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with UID '{user_data.uid}' already exists in this session."
        )

    new_user = User(name=user_data.name, uid=user_data.uid, ph_no=user_data.ph_no)
    users.add_user(new_user)
    return User_Output(**user_data.dict())

@app.delete("/users/{uid}")
async def remove_user_api(uid: str = Path(...)):
    success = users.remove_user(uid)
    if success:
        return {"message": "user removed."}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found."
        )

@app.get("/users")
async def get_users_api():
    return users.get_all_users_as_dicts()


@app.get("/users/{uid}")
async def get_user_api(uid: str = Path(...)):
    user = users.get_user_by_uid(uid)
    if user:
        return user.to_dict()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

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
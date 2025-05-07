from database.sqlite_connector import create_session
from database.sqlite_connector import Author, Book

async def add_book_db(title, genre, author_id): 
    session = create_session()
    new_auth = Book(title=title, genre=genre, author_id=author_id)
    try:
        session.add(new_auth)
        session.commit()
        return True
    except Exception as e:
        print(f"Error adding Book : {e}")
        session.rollback()
        return False
    finally:
        session.close()

async def get_all_books_db():
    session = create_session()
    try:
        books = session.query(Book.title).all()
        if not books:
            return []
        books = [name[0] for name in books]
        return books
    except Exception as e:
        print(f"Error fetching books: {e}")
        return None
    finally:
        session.close()

async def get_all_books_db_p(page: int = 1, page_size: int = 3):
    session = create_session()
    try:
        offset = (page - 1) * page_size
        books = session.query(Book.title).offset(offset).limit(page_size).all()
        books = [name[0] for name in books]
        return books
    except Exception as e:
        print(f"Error fetching books: {e}")
        return None
    finally:
        session.close()

async def get_book_data_db(ida):
    session = create_session()
    try:
        book_dets = (
            session.query(Book, Author.name, Author.email)
            .select_from(Book)
            .filter(Book.id == ida)
            .join(Author, Book.author_id == Author.id)
            .first()
        )
        
        if book_dets:
            book_dets, author_name, author_email = book_dets
            book_data = {
                "id": book_dets.id,
                "Title": book_dets.title,
                "Genre": book_dets.genre,
                "Author_id": book_dets.author_id,
                "Author_name": author_name,
                "Author_email": author_email,
            }
            return book_data
            
        else:
            print("Book not found")
            return {}

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        session.close()
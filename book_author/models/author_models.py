from database.sqlite_connector import create_session
from database.sqlite_connector import Author, Book

async def add_author_db(name, email):
    session = create_session()
    new_auth = Author(name=name, email=email)
    try:
        session.add(new_auth)
        session.commit()
        print(f"Author added: {name}")
        return True
    except Exception as e:
        print(f"Error adding Author : {e}")
        session.rollback()
        return False
    finally:
        session.close()

async def get_all_authors_db():
    session = create_session()
    try:
        authors = session.query(Author.name).all()
        authors = [name[0] for name in authors]
        return authors
    except Exception as e:
        print(f"Error fetching authors: {e}")
        return None
    finally:
        session.close()

async def get_author_data_db(ida):
    session = create_session()
    try:
        author_dets = session.query(Author).filter(Author.id == ida).first()
        if author_dets:
            author_data = {
                "id": author_dets.id,
                "name": author_dets.name,
                "email": author_dets.email,
                "books": []
            }
            
        else:
            print("Author not found")
            return {}
        
        books = (
            session.query(Book.title)
            .select_from(Author)
            .where(Author.id == ida)
            .join(Book, Author.id == Book.author_id)
            .all()
        )
        books = [title[0] for title in books]
        author_data["books"] = books
        return author_data

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        session.close()

async def get_author_books_db(ida):
    session = create_session()
    try:
        books = (
            session.query(Book.title)
            .select_from(Author)
            .where(Author.id == ida)
            .join(Book, Author.id == Book.author_id)
            .all()
        )
        books = [title[0] for title in books]
        return books
    except Exception as e:
        print(f"Error fetching books: {e}")
        return None
    finally:
        session.close()
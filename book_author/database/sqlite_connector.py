from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)

    def __init__(self, name, email):
        self.name = name
        self.email = email

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    genre = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))

    def __init__(self, title, genre, author_id):
        self.title = title
        self.genre = genre
        self.author_id = author_id


engine = create_engine('sqlite:///database/Data.db', echo=False)
Base.metadata.create_all(engine)

def create_session():
    Session = sessionmaker(bind=engine)
    return Session()
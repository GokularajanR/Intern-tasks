from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)

    def __init__(self, username, hashed_password, role):
        self.username = username
        self.hashed_password = hashed_password
        self.role = role

    def is_admin(self):
        return self.role == 'admin'

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    created_by = Column(String, ForeignKey('users.username'))

    def __init__(self, title, content, created_by):
        self.title = title
        self.content = content
        self.created_by = created_by

engine = create_engine('sqlite:///database/BlogData.db', echo=False)
Base.metadata.create_all(engine)

def create_session():
    Session = sessionmaker(bind=engine)
    return Session()
#Creates session connection

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///CRUD/database/users.db', echo=False)
Base.metadata.create_all(engine)

async def create_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
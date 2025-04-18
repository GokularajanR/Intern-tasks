#Backend CRUD ops on database
from sqlalchemy import Column, Integer, String, insert, update, delete, select
from sqlalchemy.orm import declarative_base
from database.sqlite_connector import create_session, engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'students'

    roll = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String)
    course = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

Base.metadata.create_all(engine) 

async def add_student_db(roll, name, email, age, course):
    try:
        session = await create_session()
        query = insert(User).values(roll = roll, name=name, email=email, age=age, course=course)
        session.execute(query)
        session.commit()
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error adding student: {e}")
        session.rollback()
        return False
    finally:
        session.close()

async def get_students_db():
    try:
        session = await create_session()
        user_list = []
        query = select(User)
        result = session.execute(query).scalars().all()
        for user in result:
            user_list.append({
                "roll": user.roll,
                "name": user.name,
                "email": user.email,
                "age": user.age,
                "course": user.course
            })
        return user_list
    except Exception as e:
        print(f"Error fetching students: {e}")
    finally:
        session.close()

async def get_student_by_id(key):
    try:
        session = await create_session()
        query = select(User).where(User.id == key)
        result = session.execute(query).scalars().first()
        if result: return [result]
    except Exception as e:
        print(f"Error retrieving student : {e}")
    finally:
        session.close()

async def update_student(target_roll,name, email, age, course):
    try:
        session = await create_session()
        query = update(User).where(User.roll == target_roll).values(name=name, email=email, age=age, course=course)
        session.execute(query)
        session.commit()
        return True
    except Exception as e:
        print(f"Error updating student info : {e}")
        return False
    finally:
        session.close()

async def delete_student(target_roll):
    try:
        session = await create_session()
        query = delete(User).where(User.roll == target_roll)
        session.execute(query)
        session.commit()
        return True
    except Exception as e:
        print(f"Error deleting student record : {e}")
        return False
    finally:
        session.close()
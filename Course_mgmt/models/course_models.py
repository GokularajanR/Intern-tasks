from database.sqlite_connector import create_session
from database.sqlite_connector import Course

async def add_course_db(title : str, description : str) -> bool:
    session = create_session()
    new_course = Course(title=title, description=description)
    try:
        session.add(new_course)
        session.commit()
        return True
    except Exception as e:
        print(f"Error adding course : {e}")
        session.rollback()
        return False
    finally:
        session.close()

async def remove_course(course_id):
    session = create_session()
    try:
        course = session.query(Course).filter(Course.id == course_id).first()
        if course:
            session.delete(course)
            session.commit()
            return True
        print("Course not found")
        return False
    except Exception as e:
        print(f"Error removing course : {e}")
        session.rollback()
        return False
    finally:
        session.close()
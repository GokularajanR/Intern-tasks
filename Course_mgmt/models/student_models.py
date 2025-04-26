from database.sqlite_connector import create_session
from database.sqlite_connector import Student

async def add_student_db(name, email):
    session = create_session()
    new_student = Student(name=name, email=email)
    try:
        session.add(new_student)
        session.commit()
        return True
    except Exception as e:
        print(f"Error adding student : {e}")
        session.rollback()
        return False
    finally:
        session.close()

async def remove_student(student_id):
    session = create_session()
    try:
        student = session.query(Student).filter(Student.id == student_id).first()
        if student:
            session.delete(student)
            session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error removing student : {e}")
        session.rollback()
        return False
    finally:
        session.close()
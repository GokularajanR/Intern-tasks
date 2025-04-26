from database.sqlite_connector import create_session
from database.sqlite_connector import Enrollment
from database.sqlite_connector import Course
from database.sqlite_connector import Student

async def add_enrollment_db(student_id: int, course_id: int) -> bool:
    session = create_session()
    new_enrollment = Enrollment(student_id=student_id, course_id=course_id)
    try:
        session.add(new_enrollment)
        session.commit()
        return True
    except Exception as e:
        print(f"Error adding enrollment: {e}")
        session.rollback()
        return False
    finally:
        session.close()

async def get_courses_enrolled_by_student(student_id: int):
    session = create_session()
    try:
        enrollments = (
            session.query(Course.title)
            .select_from(Enrollment)
            .filter(Enrollment.student_id == student_id)
            .join(Course, Enrollment.course_id == Course.id)
            .all()
        )
        enrollments = [title[0] for title in enrollments]
        return enrollments
    except Exception as e:
        print(f"Error fetching courses: {e}")
        return None
    finally:
        session.close()

async def get_students_enrolled_in_course(course_id: int):
    session = create_session()
    try:
        enrollments = (
            session.query(Student.name)
            .select_from(Enrollment)
            .filter(Enrollment.course_id == course_id)
            .join(Student, Enrollment.student_id == Student.id)
            .all()
        )
        enrollments = [title[0] for title in enrollments]
        return enrollments
    except Exception as e:
        print(f"Error fetching students: {e}")
        return None
    finally:
        session.close()
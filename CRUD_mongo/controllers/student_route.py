from models.student_models import Student, create_student, read_student, read_all_students, update_student, delete_student
from fastapi import APIRouter

std_router = APIRouter()

@std_router.post("/students/")
def create_student_endpoint(student: Student):
    result = create_student(student)
    return {"inserted_id": str(result.inserted_id)}

@std_router.get("/students/{student_name}")
def read_student_endpoint(student_name: str):
    student = read_student(student_name)
    return {"students": list(student)}

@std_router.get("/students/")
def read_all_students_endpoint():
    students = read_all_students()
    return {"students": students}

@std_router.put("/students/{student_id}")
def update_student_endpoint(student_id: str, updated_data: dict):
    result = update_student(student_id, updated_data)
    if result.modified_count > 0:
        return {"message": "Student updated successfully"}
    else:
        return {"message": "No student found with the given ID"}
    
@std_router.delete("/students/{student_id}")
def delete_student_endpoint(student_id: str):
    result = delete_student(student_id)
    if result.deleted_count > 0:
        return {"message": "Student deleted successfully"}
    else:
        return {"message": "No student found with the given ID"}
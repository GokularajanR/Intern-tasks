import uvicorn
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from models.student_models import add_student_db
from models.enrollment_models import add_enrollment_db, get_courses_enrolled_by_student, get_students_enrolled_in_course
from models.course_models import add_course_db

class Student(BaseModel):
    name:str
    email:str 

class Course(BaseModel):
    title:str
    description:str

class Enrollment(BaseModel):
    student_id:int
    course_id:int

app = APIRouter()

@app.post("/students/")
async def add_student(request: Student):
    result = await add_student_db(name=request.name, email=request.email)
    if not result:
        return JSONResponse(status_code=500, content={"message": "Error adding student"})
    return JSONResponse(status_code=200, content={"message": "Student added successfully", "student_id": result})

@app.post("/courses/")
async def add_course(request: Course):
    result = await add_course_db(title=request.title, description=request.description)
    if not result:
        return JSONResponse(status_code=500, content={"message": "Error adding course"})
    return JSONResponse(status_code=200, content={"message": "Course added successfully", "course_id": result})

@app.post("/enroll/")
async def add_enrollment(request: Enrollment):
    result = await add_enrollment_db(student_id=request.student_id, course_id=request.course_id)
    if not result:
        return JSONResponse(status_code=500, content={"message": "Error adding enrollment"})
    return JSONResponse(status_code=200, content={"message": "Enrollment added successfully", "enrollment_id": result})

@app.get("/students/{student_id}/courses/")
async def get_student_enrollments(student_id: int):
    enrollments = await get_courses_enrolled_by_student(student_id)
    if not enrollments:
        return JSONResponse(status_code=404, content={"message": "No enrollments found for this student"})
    return JSONResponse(status_code=200, content={"enrollments": enrollments})

@app.get("/courses/{course_id}/students/")
async def get_course_enrollments(course_id: int):
    enrollments = await get_students_enrolled_in_course(course_id)
    if not enrollments:
        return JSONResponse(status_code=404, content={"message": "No enrollments found for this course"})
    return JSONResponse(status_code=200, content={"enrollments": enrollments})
#Defines endpoints and calls methods from models

from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from models.student_models import add_student_db, get_students_db, get_student_by_id, update_student, delete_student

#Json IO Model
class Student(BaseModel):
    roll:int
    name:str
    age:int
    email:str 
    course:str

student_router = APIRouter()

#CREATE
@student_router.post("/students/add")
async def add_student(request: Student):
    result = await add_student_db(roll = request.roll, name=request.name, age=request.age, email=request.email, course=request.course)
    if not result:
        return JSONResponse(status_code=500, content={"message": "Error adding student"})
    return JSONResponse(status_code=200, content={"message": "Student added successfully", "student_id": result})


#READ
@student_router.get("/students")
async def get_students():
    get_students_list = await get_students_db()
    if not get_students_list:
        return JSONResponse(status_code=500, content={"message": "Error fetching students"})
    return JSONResponse(status_code=200, content={"students": get_students_list})

@student_router.get("/students/{roll}")
async def get_students(roll):
    get_students_list = await get_student_by_id(roll)
    if not get_students_list:
        return JSONResponse(status_code=500, content={"message": "Error fetching student"})
    return JSONResponse(status_code=200, content={"students": get_students_list})


#UPDATE
@student_router.put("/students/{roll}")
async def update_student_put(roll: int, request: Student):
    result = await update_student(target_roll=roll, name=request.name, email=request.email, age=request.age, course=request.course)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Student not found or update failed"})
    return JSONResponse(status_code=200, content={"message": "Student updated successfully"})



#DELETE
@student_router.delete("/students/{roll}")
async def delete_student_by_roll(roll: int):
    result = await delete_student(target_roll=roll)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Student not found or deletion failed"})
    return JSONResponse(status_code=200, content={"message": f"Student with roll {roll} deleted successfully"})
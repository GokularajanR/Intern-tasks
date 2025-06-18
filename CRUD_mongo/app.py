from pymongo import MongoClient
from pydantic import BaseModel
from fastapi import FastAPI
from bson import ObjectId

class Student(BaseModel):
    name: str
    email: str
    age: int

URL = "mongodb+srv://gokul26092004:gulgul@gul.wmd0umx.mongodb.net/?retryWrites=true&w=majority&appName=gul"

client = MongoClient(URL)
db = client['gul']
collection = db['students']

def create_student(student: Student):
    return collection.insert_one(student.dict())

def read_student(student_name: str):
    result = collection.find({"name": student_name})
    return [transform_id(doc) for doc in result]

def read_all_students():
    return [transform_id(doc) for doc in collection.find()]

def transform_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc


def update_student(student_id: str, updated_data: dict):
    return collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": updated_data}
    )

def delete_student(student_id: str):
    return collection.delete_one({"_id": ObjectId(student_id)})



app = FastAPI()
@app.post("/students/")
def create_student_endpoint(student: Student):
    result = create_student(student)
    return {"inserted_id": str(result.inserted_id)}

@app.get("/students/{student_name}")
def read_student_endpoint(student_name: str):
    student = read_student(student_name)
    return {"students": list(student)}

@app.get("/students/")
def read_all_students_endpoint():
    students = read_all_students()
    return {"students": students}

@app.put("/students/{student_id}")
def update_student_endpoint(student_id: str, updated_data: dict):
    result = update_student(student_id, updated_data)
    if result.modified_count > 0:
        return {"message": "Student updated successfully"}
    else:
        return {"message": "No student found with the given ID"}
    
@app.delete("/students/{student_id}")
def delete_student_endpoint(student_id: str):
    result = delete_student(student_id)
    if result.deleted_count > 0:
        return {"message": "Student deleted successfully"}
    else:
        return {"message": "No student found with the given ID"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
from bson import ObjectId
from pymongo import MongoClient
from pydantic import BaseModel

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
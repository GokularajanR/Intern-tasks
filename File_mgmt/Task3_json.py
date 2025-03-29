import json

student_info = {
    "name": "John Doe",
    "age": 21,
    "skills": ["Python", "FastAPI"],
    "internship": "Ongoing"
}

with open("data.json", "w") as file:
    json.dump(student_info, file)

with open("data.json", "r") as file:
    data = json.load(file)

print(data)
from fastapi import FastAPI
from controllers.student_route import student_router


#test again
app = FastAPI()
app.include_router(student_router)
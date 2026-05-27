from fastapi import (
    FastAPI,
    HTTPException,
    status
)
from pydantic import BaseModel, Field, EmailStr
from typing import List

app= FastAPI(
    title="My API",
    description="This is a sample API built with FastAPI",
    version="1.0.0"
)

class StudentCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr
    program: str = Field(..., example="Computer Science")
    active: bool

class Student(StudentCreate):
    id: int

students = [
    {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "program": "Computer Science",
    "active": True
    },
    {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "program": "Mathematics",
    "active": False
    },
    {
    "id": 3,
    "name": "Alice Johnson",
    "email": "alice.johnson@example.com",
    "program": "Physics",
    "active": True
    }, 
    {
    "id": 4,
    "name": "Bob Brown",
    "email": "bob.brown@example.com",
    "program": "Biology",
    "active": True
    },
    {
    "id": 5,
    "name": "Charlie Wilson",
    "email": "charlie.wilson@example.com",
    "program": "Chemistry",
    "active": False
    }
]

@app.get("/")
def home():
    return {
        "message": "Welcome to my API!",
        "endpoints": [
            "POST /students",
            "GET /students/{id}",
            "GET /students?active=true",
            "GET /students?active=false"
        ]
    }

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentCreate):
    new_id = max(student["id"] for student in students) + 1
    new_student = {
        "id": new_id,
        "name": student_data.name,
        "email": student_data.email,
        "program": student_data.program,
        "active": student_data.active
    }
    students.append(new_student)
    return new_student

@app.get("/students", response_model=List[Student])
def get_students(active: bool = None):
    if active is None:
        return students
    return [student for student in students if student["active"] == active]


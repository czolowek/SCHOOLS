from pydantic import BaseModel, Field
from typing import Optional

class Message(BaseModel):
    content: str = Field(..., max_length=1000)

class Student(BaseModel):
    id: Optional[int]
    name: str

class Teacher(BaseModel):
    id: Optional[int]
    name: str

class Course(BaseModel):
    id: Optional[int]
    title: str
    teacher_id: int

class Enrollment(BaseModel):
    student_id: int
    course_id: int
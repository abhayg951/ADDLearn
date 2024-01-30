from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from fastapi import Form
from dataclasses import dataclass

class CourseSchema(BaseModel):
    id: int
    course_name: str
    description: str
    teacher: str
    img_url: str
    course_code: str
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True

class CourseResponse(BaseModel):
    Course: CourseSchema
    enrollments: int

    class Config:
        from_attributes = True


@dataclass
class CreateCourse:
    course_name: str = Form(...)
    teacher: str = Form(...)
    description: Optional[str] = Form(...)
    course_code: str = Form(...)
    is_published: bool = Form(...)
    category: int = Form(...)

    class Config:
        from_attributes = True


class Perform_enroll(BaseModel):
    enroll_dir: int
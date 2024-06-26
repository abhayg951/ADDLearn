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
    updated_at : Optional[str]
    category: int

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
    description: str = Form(None)
    course_code: str = Form(...)
    is_published: bool = Form(...)
    category: int = Form(...)

    class Config:
        from_attributes = True


class Perform_enroll(BaseModel):
    enroll_dir: int


@dataclass
class UpdateCourse:
    course_name: str = Form(None)
    teacher: str = Form(None)
    description: str = Form(None)
    course_code: str = Form(None)
    is_published: bool = Form(None)
    category: int = Form(None)

    class Config:
        from_attributes = True
    

class RateCourseSchema(BaseModel):
    remarks: Optional[str]
    rating: int = 1

    class Config:
        from_attributes = True

class RateCourseResponse(BaseModel):
    id: int
    user: int
    course: int
    remarks: Optional[str]
    rating: int

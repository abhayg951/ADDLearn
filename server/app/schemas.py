from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Annotated
from fastapi import Form, UploadFile
from dataclasses import dataclass

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    role: str
    education: str
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    id: int
    name: str
    education: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class CourseSchema(BaseModel):
    id: int
    course_name: str
    description: str
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
    description: Optional[str] = Form(...)
    course_code: str = Form(...)
    is_published: bool = Form(...)
    category: int = Form(...)


class Perform_enroll(BaseModel):
    enroll_dir: int
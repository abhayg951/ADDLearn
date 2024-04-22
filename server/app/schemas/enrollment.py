from pydantic import BaseModel
from .courses import CourseSchema
from datetime import datetime

class EnrollmentSchema(BaseModel):
    course: CourseSchema
    course_id: int
    enroll_at: datetime
    completed_chapters: list
    is_completed: bool
    user_id: int

    class Config:
        from_attributes = True
from pydantic import BaseModel
from dataclasses import dataclass
from fastapi import Form
from typing import Optional
from datetime import datetime

class ChapterSchema(BaseModel):
    id: int
    title : str
    description: Optional[str]
    chapter_no: int
    video_url: str
    pdf_url: str
    is_published: bool
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True

@dataclass
class CreateChapter:
    title: str = Form(...)
    description: str = Form(None)
    chapter_no: int = Form(...)
    is_published: bool = Form(False)

    class Config:
        from_attributes = True

@dataclass
class UpdateChapter:
    title: str = Form(None)
    description: str = Form(None)
    chapter_no: int = Form(None)
    is_published: bool = Form(None)

    class Config:
        from_attributes = True

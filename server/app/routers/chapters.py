from fastapi import Depends, APIRouter, HTTPException, File, status, UploadFile
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..oauth2 import get_current_user
from ..schemas import chapters
from ..cloudinary import uploadfile

routers = APIRouter(
    tags=[
        'Chapters'
    ],
    prefix="/chapter"
)

async def upload_module(notes, chapter_no) -> str:
    if notes is None:
        return ""
    url = await uploadfile.upload_modules(notes.file, chapter_no, notes.filename)
    return url

async def upload_Video(video, chapter_no) -> str:
    if video is None:
        return ""
    url = await uploadfile.upload_video(video.file, chapter_no, video.filename)
    return url

@routers.post('/course/{id}/create', response_model=chapters.ChapterSchema, status_code=status.HTTP_201_CREATED)
async def upload_chapter(id: int, 
                   notes: UploadFile = File(None),
                   video: UploadFile = File(None), 
                   chapter_schema: chapters.CreateChapter = Depends(), 
                   db: Session = Depends(get_db), 
                   current_user: models.User = Depends(get_current_user)):
    
    if str(current_user.role) != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not allowed to upload chapter")
    
    get_course_id = db.query(models.Course).filter(models.Course.id == id).first()
    if get_course_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course of id {id} not found")

    pdf_url = await upload_module(notes, chapter_schema.chapter_no)
    video_url = await upload_Video(video, chapter_schema.chapter_no)

    chapter_dict = chapter_schema.__dict__
    chapter_dict['video_url'] = video_url
    chapter_dict['pdf_url'] = pdf_url
    chapter_dict['course_id'] = id

    new_chapter = models.Chapters(**chapter_dict)
    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)
    return new_chapter

@routers.get('/course/{id}')
def get_course_chapters(id: int, db: Session = Depends(get_db)):

    get_course_id = db.query(models.Course).filter(models.Course.id == id).first()
    if get_course_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course of id {id} not found")
    
    course_data =  db.query(models.Chapters).filter(models.Chapters.course_id == id).order_by(models.Chapters.chapter_no.asc()).all()
    if not course_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No chapters found of course {id}")
    return course_data
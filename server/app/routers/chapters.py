from fastapi import Depends, APIRouter, HTTPException, File, status, UploadFile, Path
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


@routers.get('/course/{course_id}')
def get_course_chapters(course_id: int, db: Session = Depends(get_db)):

    get_course_id = db.query(models.Course).filter(models.Course.id == course_id).first()
    if get_course_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course of id {course_id} not found")
    
    course_data =  db.query(models.Chapters).filter(models.Chapters.course_id == course_id).order_by(models.Chapters.chapter_no.asc()).all()
    if not course_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No chapters found of course {course_id}")
    return course_data

@routers.get('/{chapter_id}', response_model=chapters.ChapterSchema)
def get_single_chapter(chapter_id: int, db: Session = Depends(get_db)):
    
    chapter_data =  db.query(models.Chapters).filter(models.Chapters.id == chapter_id).first()
    if not chapter_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Chapter not found")
    return chapter_data

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

@routers.post('/course/{course_id}/create', response_model=chapters.ChapterSchema, status_code=status.HTTP_201_CREATED)
async def upload_chapter(course_id: int, 
                   notes: UploadFile = File(None),
                   video: UploadFile = File(None), 
                   chapter_schema: chapters.CreateChapter = Depends(), 
                   db: Session = Depends(get_db), 
                   current_user: models.User = Depends(get_current_user)):
    
    if str(current_user.role) != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not allowed to upload chapter")
    
    get_course_id = db.query(models.Course).filter(models.Course.id == course_id).first()
    if get_course_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course of id {course_id} not found")

    # resources_url = await upload_module(notes, chapter_schema.chapter_no)
    # video_url = await upload_Video(video, chapter_schema.chapter_no)

    chapter_dict = chapter_schema.__dict__
    # chapter_dict['video_url'] = video_url
    # chapter_dict['resources_url'] = resources_url
    chapter_dict['course_id'] = course_id

    new_chapter = models.Chapters(**chapter_dict)
    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)
    return new_chapter


@routers.patch('/course/{course_id}/update/{chapter_id}', status_code=status.HTTP_201_CREATED)
async def update_chapter(course_id: str,
                         chapter_id: str,
                         notes: UploadFile = File(None),
                         video: UploadFile = File(None), 
                         chapter_schema: chapters.UpdateChapter = Depends(), 
                         db: Session = Depends(get_db), 
                         current_user: models.User = Depends(get_current_user)):
    
    if not course_id.isnumeric() or not chapter_id.isnumeric():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide valid param")
    if str(current_user.role) != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not allowed to update chapter")
    
    get_course_id = db.query(models.Course).filter(models.Course.id == course_id).first()
    if get_course_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course of id {course_id} not found")
    
    get_chapter = db.query(models.Chapters).filter(models.Chapters.id == chapter_id, models.Chapters.course_id == course_id)
    if get_chapter.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Chapter not found")
    
    try:
        chapter_dict = chapter_schema.__dict__

        if video is not None:
            video_url = await upload_Video(video, chapter_schema.chapter_no)
            chapter_dict['video_url'] = video_url
        
        if notes is not None:
            pdf_url = await upload_module(notes, chapter_schema.chapter_no)
            chapter_dict['pdf_url'] = pdf_url
        
        filtered_dict = {key: value for key, value in chapter_dict.items() if value is not None}

        get_chapter.update(filtered_dict, synchronize_session=False)
        db.commit()
        db.refresh(get_chapter.first())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Something went wrong")    
    return get_chapter.first()

@routers.delete("/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chapter(chapter_id: int, db: Session = Depends(get_db), get_user: models.User = Depends(get_current_user)):
    if str(get_user.role) != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not allowed to delete this chapter")
    find_chapter = db.query(models.Chapters).filter(models.Chapters.id == chapter_id)
    if find_chapter.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter Not found")
    find_chapter.delete()
    db.commit()
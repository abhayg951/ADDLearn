from fastapi import APIRouter, Depends, HTTPException, status, File, Form
from sqlalchemy import func
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas
from typing import List, Optional, Annotated
from ..cloudinary.uploadfile import upload_thumbnail

routers = APIRouter(
    tags=['Courses'],
    prefix="/course"
)

@routers.get("", status_code=status.HTTP_200_OK, response_model=List[schemas.CourseResponse])
def get_all_courses(db: Session = Depends(get_db), q: Optional[str]= ""):

    if q != "":
        all_courses = db.query(models.Course, func.count(models.Enrollments.course_id).label("enrollments")).join(
            models.Enrollments, models.Enrollments.course_id == models.Course.id, isouter=True).group_by(
                models.Course.id).filter(
                    models.Course.course_name.ilike(q)).all()
        return all_courses
    
    else:
        all_courses = db.query(models.Course, func.count(models.Enrollments.course_id).label("enrollments")).join(
            models.Enrollments, models.Enrollments.course_id == models.Course.id, isouter=True).group_by(
                models.Course.id).all()
        return all_courses

@routers.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.CourseSchema)
def get_single_course(id: int, db: Session = Depends(get_db)):

    course = db.query(models.Course).filter(models.Course.id == id)

    find_course = course.first()
    if not find_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id '{id}' not found")
    
    return find_course


@routers.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.CourseSchema)
async def upload_course(img: bytes = File(None), course_schema: schemas.CreateCourse = Depends(), db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if (str(current_user.role) == "student" or str(current_user.role) == "teacher"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to upload a course")
    print(current_user.role)
    if img is None:
        img_url = ""
    else:
        img_url = upload_thumbnail(img)
    print("----------------------------------------")
    new_course = models.Course(
        course_name = course_schema.course_name,
        description = course_schema.description,
        img_url = img_url,
        is_published = course_schema.is_published,
        course_code = course_schema.course_code,
        category = course_schema.category
        )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@routers.post("/enroll/{id}")
def course_enrollment(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} does not exist")
    find_enrollment_query = db.query(models.Enrollments).filter(models.Enrollments.course_id == id, models.Enrollments.user_id == current_user.id)
    find_enrollment = find_enrollment_query.first()
    if find_enrollment:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already enrolled in course {id}")
    enroll = models.Enrollments(course_id = id, user_id=current_user.id)
    db.add(enroll)
    db.commit()
    db.refresh(enroll)
    return enroll

@routers.post("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.CourseSchema)
async def upload_course(img: bytes = File(None), course_schema: schemas.CreateCourse = Depends(), db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if (str(current_user.role) == "student" or str(current_user.role) == "teacher"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to upload a course")
    print(current_user.role)
    img_url = upload_thumbnail(img)
    new_course = models.Course(
        course_name = course_schema.course_name,
        description = course_schema.description,
        img_url = img_url,
        is_published = course_schema.is_published,
        course_code = course_schema.course_code,
        category = course_schema.category
        )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course
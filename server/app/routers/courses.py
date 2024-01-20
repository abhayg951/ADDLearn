from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas
from typing import List


routers = APIRouter(
    tags=['Courses'],
    prefix="/course"
)

@routers.get("", response_model=List[schemas.CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    # all_courses = db.query(models.Courses).all()
    all_courses = db.query(models.Course, func.count(models.Enrollments.course_id).label("enrollments")).join(
        models.Enrollments, models.Enrollments.course_id == models.Course.id, isouter=True).group_by(models.Course.id).all()
    print(all_courses)
    return all_courses
@routers.post("")
def upload_course(course_schema: schemas.CreateCourse, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if (str(current_user.role) == "student" or str(current_user.role) == "teacher"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to upload a course")
    # print(current_user.role)
    new_course = models.Course(**course_schema.model_dump())
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
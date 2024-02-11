from fastapi import APIRouter, Depends, HTTPException, Response, status, File, Form
from sqlalchemy import func
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, oauth2
from ..schemas import courses
from typing import List, Optional, Annotated
from ..cloudinary.uploadfile import upload_thumbnail
from datetime import datetime

routers = APIRouter(
    tags=['Courses'],
    prefix="/course"
)

@routers.get("", status_code=status.HTTP_200_OK, response_model=List[courses.CourseResponse])
def get_all_courses(db: Session = Depends(get_db), 
                    pub: str = "",
                    q: Optional[str]= "",
                    cc: Optional[str] = "",
                    cate: Optional[int] = None,
                    limit: int = 10, 
                    skip: int = 0):
    '''By Default this will return all the courses. To view the list of published courses provide the 'pub' param with value equal to 'published' '''

    if pub == "":
        if cate is not None:
            all_courses = db.query(models.Course, func.count(models.Enrollments.course_id).label("enrollments")).join(
                models.Enrollments, models.Enrollments.course_id == models.Course.id, isouter=True).group_by(
                    models.Course.id).filter(models.Course.category == cate,
                                            models.Course.course_name.ilike(f"%{q}%"),
                                            models.Course.course_code.ilike(f"%{cc}%")).limit(limit).offset(skip).all()
            return all_courses
        else:
            all_courses = db.query(models.Course, func.count(models.Enrollments.course_id).label("enrollments")).join(
                    models.Enrollments, models.Enrollments.course_id == models.Course.id, isouter=True).group_by(
                        models.Course.id).filter(models.Course.course_name.ilike(f"%{q}%"),
                                                models.Course.course_code.ilike(f"%{cc}%")).limit(limit).offset(skip).all()
            return all_courses
    
    elif pub == "published":
        if cate is not None:
            all_courses = db.query(models.Course, func.count(models.Enrollments.course_id).label("enrollments")).join(
            models.Enrollments, models.Enrollments.course_id == models.Course.id, isouter=True).group_by(
                models.Course.id).filter(models.Course.is_published == True,
                                        models.Course.category == cate,
                                        models.Course.course_name.ilike(f"%{q}%"),
                                        models.Course.course_code.ilike(f"%{cc}%")).limit(limit).offset(skip).all()
            return all_courses
        else:
            all_courses = db.query(models.Course, func.count(models.Enrollments.course_id).label("enrollments")).join(
                models.Enrollments, models.Enrollments.course_id == models.Course.id, isouter=True).group_by(
                    models.Course.id).filter(models.Course.is_published == True,
                                            models.Course.course_name.ilike(f"%{q}%"),
                                            models.Course.course_code.ilike(f"%{cc}%")).limit(limit).offset(skip).all()
            return all_courses
@routers.get('/{id}', status_code=status.HTTP_200_OK, response_model=courses.CourseSchema)
def get_single_course(id: str, db: Session = Depends(get_db)):
    '''This will allow you to fetch the single course using the course id'''
    if not id.isnumeric():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid param")
    
    course = db.query(models.Course).filter(models.Course.id == id)

    find_course = course.first()
    if not find_course:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail={})
    
    return find_course


@routers.post("", status_code=status.HTTP_201_CREATED, response_model=courses.CourseSchema)
async def upload_course(img: bytes = File(None), course_schema: courses.CreateCourse = Depends(), db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    ''' This will allow you to upload the course. Only admin can upload the course. '''
    try:
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
            teacher = course_schema.teacher,
            img_url = img_url,
            is_published = course_schema.is_published,
            course_code = course_schema.course_code,
            category = course_schema.category
            )
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Some error occur")
    return new_course

@routers.post("/enroll/{id}")
def course_enrollment(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if not id.isnumeric():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid param")
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


@routers.patch("/{id}", status_code=status.HTTP_200_OK, response_model=courses.CourseSchema)
async def update_course(id: str, img: bytes = File(None), course_schema: courses.UpdateCourse = Depends(), db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if not id.isnumeric():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid param")
    try: 
        single_course = db.query(models.Course).filter(models.Course.id == id)
        updated_course = single_course.first()
        if updated_course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"course with id {id} does not exists")
        if (str(current_user.role).lower() == "student" or str(current_user.role).lower() == "teacher"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update a course")
        print(current_user.role)
        
        course_dict = course_schema.__dict__
        if img is not None:
            img_url = upload_thumbnail(img)
            course_dict["img_url"] = img_url
        course_dict["updated_at"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(type(course_dict))
        filtered_dict = {key: value for key, value in course_dict.items() if value is not None}
        print(course_dict)
        single_course.update(filtered_dict, synchronize_session=False)
        db.commit()
        db.refresh(single_course.first())
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
    
    return single_course.first()


@routers.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(cid: str, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if not cid.isnumeric():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid param")
    find_course = db.query(models.Course).filter(models.Course.id == cid)
    if find_course.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course doesn't exist")
    if (str(current_user.role).lower() == "student" or str(current_user.role).lower() == "teacher"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete a course")
    find_course.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
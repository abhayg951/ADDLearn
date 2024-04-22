from fastapi import Response, APIRouter, Depends, HTTPException, status
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import courses
from .. import models
from .. import oauth2

routers = APIRouter(
    tags=["Course Rating"],
    prefix="/rate"
)

# TODO: Create the rating system

@routers.post("/{course_id}", response_model=courses.RateCourseResponse)
def rate_course(course_id: int,
                rate_schema: courses.RateCourseSchema, 
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    get_enroll = db.query(models.Enrollments).filter(models.Enrollments.user_id == current_user.id, models.Enrollments.course_id == course_id)
    # check enrollment
    print(get_enroll.first())
    if get_enroll.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You must enroll in the course")

    if not get_enroll.first().is_completed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You must complete the course")
    
    get_rate = db.query(models.Ratings).filter(models.Ratings.course == course_id, models.Ratings.user == current_user.id).first()
    if get_rate:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already rated the course")

    print(rate_schema.model_dump())
    user_rating = models.Ratings(**rate_schema.model_dump(), course = course_id, user = current_user.id)
    db.add(user_rating)
    db.commit()
    db.refresh(user_rating)
    return user_rating